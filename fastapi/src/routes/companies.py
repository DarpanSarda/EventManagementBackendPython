from fastapi import APIRouter , status , Depends
from fastapi.responses import JSONResponse
from schemas.companiesSchema import CompaniesAdmin
from services.companiesService import CompaniesService
from bson import ObjectId
from typing import List
from dependency.auth import admin_only

companyRouter = APIRouter(
    prefix="/companies",
    tags=["companies"],
)

def convert_objectid_to_str(data):
    """Recursively convert ObjectId fields in a dictionary to strings."""
    if isinstance(data, dict):
        return {k: convert_objectid_to_str(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_objectid_to_str(item) for item in data]
    elif isinstance(data, ObjectId):
        return str(data)  # Convert ObjectId to string
    return data  # Return as is if it's not an ObjectId

@companyRouter.post("/", dependencies=[Depends(admin_only)] , response_model=CompaniesAdmin)
async def create_company(company: CompaniesAdmin):
    """
    Create a new company - Admin only endpoint
    
    Args:
        company (CompaniesAdmin): The company data to be created
        
    Returns:
        JSONResponse: Created company data or error message
    """
    try:
        new_company =await CompaniesService.AddCompany(company)
        if new_company:
            new_company = convert_objectid_to_str(new_company)
            response = {
                "status": "success",
                "data": new_company,
                "message": "Company created successfully"
            }
            return JSONResponse(content=response, status_code=status.HTTP_201_CREATED)
        
        response = {
            "status": "failed",
            "message": "Failed to create company"
        }
        return JSONResponse(content=response, status_code=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        response = {
            "status": "error",
            "message": str(e)
        }
        return JSONResponse(content=response, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@companyRouter.get("/", response_model=List[CompaniesAdmin])
async def get_all_company():
    """
    Get all companies - Admin only endpoint
    
    Returns:
        JSONResponse: List of companies or error message
    """
    try:
        companies = await CompaniesService.getCompanies()
        if companies:
            companies = convert_objectid_to_str(companies)  # Convert ObjectId to string
            response = {
                "status": "success",
                "data": companies,
                "message": "Companies retrieved successfully"
            }
            return JSONResponse(content=response, status_code=status.HTTP_200_OK)
        
        response = {
            "status": "success",
            "data": [],
            "message": "No companies found"
        }
        return JSONResponse(content=response, status_code=status.HTTP_200_OK)
        
    except Exception as e:
        response = {
            "status": "error",
            "message": str(e)
        }
        return JSONResponse(content=response, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)