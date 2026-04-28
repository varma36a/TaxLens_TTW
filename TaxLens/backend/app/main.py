from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import upload, tax, compare, explain, scenario, sessions
from app.database.mongodb import ensure_indexes

app = FastAPI(title="Tax Lens API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",
        "http://127.0.0.1:4200"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router)
app.include_router(tax.router)
app.include_router(compare.router)
app.include_router(explain.router)
app.include_router(scenario.router)
app.include_router(sessions.router)

@app.on_event("startup")
async def startup():
    await ensure_indexes()
