from fastapi import APIRouter

router = APIRouter(
    prefix="/tax",
    tags=["Tax"]
)

@router.get("/")
async def tax_home():
    return {"message": "Tax route active"}

@router.post("/calculate")
async def calculate_tax():
    return {"message": "Tax calculation endpoint ready"}