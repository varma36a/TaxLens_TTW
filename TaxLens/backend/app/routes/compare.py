from fastapi import APIRouter, HTTPException, Query
from datetime import datetime
import asyncio
from pymongo.collation import Collation
from pymongo.errors import PyMongoError
from app.database.mongodb import db
from app.services.foundry_agent_service import generate_tax_explanation

router = APIRouter(prefix="/compare", tags=["Compare"])
CASE_INSENSITIVE_COLLATION = Collation(locale="en", strength=2)
COMPARISON_FIELDS = (
    "company_name",
    "entity_type",
    "state_code",
    "tax_year",
    "gross_income",
    "deductions",
    "credits",
    "federal_tax",
    "state_tax",
    "total_tax",
    "effective_tax_rate",
)

def comparison_view(company: dict) -> dict:
    return {field: company.get(field) for field in COMPARISON_FIELDS if field in company}

@router.get("/companies")
async def compare_companies(
    company1: str = Query(...),
    company2: str = Query(...)
):
    company1 = company1.strip()
    company2 = company2.strip()

    try:
        c1, c2 = await asyncio.gather(
            db.tax_results.find_one(
                {"company_name": company1},
                {"_id": 0},
                collation=CASE_INSENSITIVE_COLLATION
            ),
            db.tax_results.find_one(
                {"company_name": company2},
                {"_id": 0},
                collation=CASE_INSENSITIVE_COLLATION
            )
        )
    except PyMongoError as exc:
        raise HTTPException(status_code=503, detail="Database unavailable") from exc

    if not c1 or not c2:
        raise HTTPException(status_code=404, detail="One or both companies not found")

    prompt = f"""
    Compare these corporations:
    Company 1: {comparison_view(c1)}
    Company 2: {comparison_view(c2)}

    Analyze:
    - Federal tax burden
    - State tax burden
    - Total tax
    - Effective tax rate
    - Tax optimization opportunities
    - Entity efficiency
    """

    try:
        summary = await generate_tax_explanation(prompt)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    timestamp = datetime.utcnow()

    try:
        await asyncio.gather(
            db.comparisons.insert_one({
                "company_1": company1,
                "company_2": company2,
                "summary": summary,
                "timestamp": timestamp
            }),
            db.sessions.insert_one({
                "session_type": "comparison",
                "company_1": company1,
                "company_2": company2,
                "summary": summary,
                "timestamp": timestamp
            })
        )
    except PyMongoError as exc:
        raise HTTPException(status_code=503, detail="Database unavailable") from exc

    return {
        "company_1": c1,
        "company_2": c2,
        "comparison_summary": summary
    }

@router.get("/list")
async def list_companies():
    try:
        companies = await db.tax_results.find({}, {"company_name": 1, "_id": 0}).to_list(100)
    except PyMongoError as exc:
        raise HTTPException(status_code=503, detail="Database unavailable") from exc
    return companies
