from fastapi import APIRouter, UploadFile, File, HTTPException
import pandas as pd
from datetime import datetime
import asyncio
from pymongo.errors import PyMongoError
from app.services.tax_engine import calculate_total_tax
from app.database.mongodb import db

router = APIRouter(prefix="/upload", tags=["Upload"])

REQUIRED_COLUMNS = {
    "CompanyName",
    "GrossIncome",
    "Deductions",
    "EntityType",
    "StateCode",
    "TaxYear",
    "NOLCarryforward",
    "EstimatedPayments",
    "Credits",
}

@router.post("/upload-excel")
async def upload_excel(file: UploadFile = File(...)):
    try:
        df = await asyncio.to_thread(pd.read_excel, file.file)
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Invalid Excel file") from exc

    missing_columns = sorted(REQUIRED_COLUMNS - set(df.columns))
    if missing_columns:
        raise HTTPException(
            status_code=400,
            detail=f"Missing required columns: {', '.join(missing_columns)}",
        )

    results = []
    documents = []
    timestamp = datetime.utcnow()

    for _, row in df.iterrows():
        company = {
            "company_name": row["CompanyName"],
            "gross_income": row["GrossIncome"],
            "deductions": row["Deductions"],
            "entity_type": row["EntityType"],
            "state_code": row["StateCode"],
            "tax_year": row["TaxYear"],
            "nol_carryforward": row["NOLCarryforward"],
            "estimated_payments": row["EstimatedPayments"],
            "credits": row["Credits"]
        }

        try:
            tax_result = calculate_total_tax(type("Company", (), company))
        except (KeyError, TypeError, ValueError) as exc:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid tax data for company '{company['company_name']}'",
            ) from exc

        documents.append({
            **company,
            **tax_result,
            "timestamp": timestamp
        })

        results.append({
            **company,
            **tax_result
        })

    writes = [
        db.sessions.insert_one({
            "session_type": "upload",
            "file_name": file.filename,
            "records_processed": len(results),
            "timestamp": timestamp
        })
    ]
    if documents:
        writes.append(db.tax_results.insert_many(documents, ordered=False))

    persistence_warning = None
    try:
        await asyncio.gather(*writes)
    except PyMongoError as exc:
        persistence_warning = f"Results calculated but not saved: {exc.__class__.__name__}"

    response = {
        "message": "File processed successfully",
        "records_processed": len(results),
        "results": results
    }
    if persistence_warning:
        response["warning"] = persistence_warning

    return response
