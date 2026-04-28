from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
import asyncio
from pymongo.collation import Collation
from pymongo.errors import PyMongoError
from app.database.mongodb import db
from app.services.tax_engine import calculate_total_tax
from app.services.foundry_agent_service import generate_tax_explanation

router = APIRouter(prefix="/scenario", tags=["Scenario"])
CASE_INSENSITIVE_COLLATION = Collation(locale="en", strength=2)

class ScenarioRequest(BaseModel):
    company_name: str
    new_state_code: str = None
    new_entity_type: str = None
    additional_deductions: float = 0
    additional_credits: float = 0

@router.post("/what-if")
async def what_if_analysis(request: ScenarioRequest):
    company_name = request.company_name.strip()

    try:
        company = await db.tax_results.find_one(
            {"company_name": company_name},
            {"_id": 0},
            collation=CASE_INSENSITIVE_COLLATION
        )
    except PyMongoError as exc:
        raise HTTPException(status_code=503, detail="Database unavailable") from exc

    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    company["state_code"] = request.new_state_code or company["state_code"]
    company["entity_type"] = request.new_entity_type or company["entity_type"]
    company["deductions"] += request.additional_deductions
    company["credits"] += request.additional_credits

    try:
        recalculated = calculate_total_tax(type("Company", (), company))
    except (KeyError, TypeError, ValueError) as exc:
        raise HTTPException(status_code=400, detail="Invalid scenario tax data") from exc

    prompt = f"""
    Original Company: {company_name}
    Updated Structure: {company}
    New Tax Outcome: {recalculated}

    Explain:
    - Tax savings or increase
    - State tax effects
    - Entity effects
    - Strategic recommendations
    """

    try:
        summary = await generate_tax_explanation(prompt)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    timestamp = datetime.utcnow()

    try:
        await asyncio.gather(
            db.what_if_scenarios.insert_one({
                "company_name": company_name,
                "updated_inputs": company,
                "results": recalculated,
                "summary": summary,
                "timestamp": timestamp
            }),
            db.sessions.insert_one({
                "session_type": "scenario",
                "company_name": company_name,
                "updated_inputs": company,
                "results": recalculated,
                "summary": summary,
                "timestamp": timestamp
            })
        )
    except PyMongoError as exc:
        raise HTTPException(status_code=503, detail="Database unavailable") from exc

    return {
        "updated_company": company,
        "scenario_results": recalculated,
        "scenario_summary": summary
    }
