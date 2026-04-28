from fastapi import APIRouter, HTTPException
from pymongo.errors import PyMongoError
from app.database.mongodb import db

router = APIRouter(prefix="/sessions", tags=["Sessions"])

@router.get("/history")
async def get_all_sessions(limit: int = 100):
    try:
        sessions = await db.sessions.find(
            {},
            {"_id": 0}
        ).sort("timestamp", -1).to_list(limit)
    except PyMongoError as exc:
        raise HTTPException(status_code=503, detail="Database unavailable") from exc

    return {
        "count": len(sessions),
        "sessions": sessions
    }

@router.get("/uploads")
async def get_uploads(limit: int = 50):
    try:
        uploads = await db.tax_results.find({}, {"_id": 0}).to_list(limit)
    except PyMongoError as exc:
        raise HTTPException(status_code=503, detail="Database unavailable") from exc
    return {"count": len(uploads), "uploads": uploads}

@router.get("/comparisons")
async def get_comparisons(limit: int = 50):
    try:
        comparisons = await db.comparisons.find({}, {"_id": 0}).to_list(limit)
    except PyMongoError as exc:
        raise HTTPException(status_code=503, detail="Database unavailable") from exc
    return {"count": len(comparisons), "comparisons": comparisons}

@router.get("/scenarios")
async def get_scenarios(limit: int = 50):
    try:
        scenarios = await db.what_if_scenarios.find({}, {"_id": 0}).to_list(limit)
    except PyMongoError as exc:
        raise HTTPException(status_code=503, detail="Database unavailable") from exc
    return {"count": len(scenarios), "scenarios": scenarios}
