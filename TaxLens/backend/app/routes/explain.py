from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
import asyncio
from app.services.foundry_agent_service import generate_tax_explanation
from app.database.mongodb import db

router = APIRouter(prefix="/explain", tags=["Explain"])

class ExplainRequest(BaseModel):
    query: str

@router.post("/tax")
async def explain_tax(request: ExplainRequest):
    try:
        explanation = await generate_tax_explanation(request.query)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    timestamp = datetime.utcnow()

    await asyncio.gather(
        db.chat_history.insert_one({
            "query": request.query,
            "response": explanation,
            "timestamp": timestamp
        }),
        db.sessions.insert_one({
            "session_type": "explanation",
            "query": request.query,
            "response": explanation,
            "timestamp": timestamp
        })
    )

    return {
        "query": request.query,
        "explanation": explanation
    }
