from fastapi import APIRouter

companyRouter = APIRouter(
    prefix="/companies",
    tags=["companies"],
)

@companyRouter.post("/")
async def create_company():
    pass