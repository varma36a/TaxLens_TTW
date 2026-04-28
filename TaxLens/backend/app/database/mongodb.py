from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING, DESCENDING
from pymongo.collation import Collation
from pymongo.errors import PyMongoError
import logging
from app.config.settings import settings

logger = logging.getLogger(__name__)

client = AsyncIOMotorClient(
    settings.mongodb_uri,
    serverSelectionTimeoutMS=settings.mongodb_server_selection_timeout_ms,
)
db = client[settings.database_name]

CASE_INSENSITIVE_COLLATION = Collation(locale="en", strength=2)

async def ensure_indexes():
    try:
        await db.tax_results.create_index(
            [("company_name", ASCENDING)],
            name="company_name_ci",
            collation=CASE_INSENSITIVE_COLLATION,
            background=True,
        )
        await db.sessions.create_index([("timestamp", DESCENDING)], background=True)
        await db.comparisons.create_index([("timestamp", DESCENDING)], background=True)
        await db.what_if_scenarios.create_index([("timestamp", DESCENDING)], background=True)
    except PyMongoError as exc:
        logger.warning("MongoDB indexes were not created: %s", exc)
