from eventapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from schemas.faqsSchema import FAQsSchemaReq
from services.faqService import FAQService
from bson import ObjectId
from typing import List
from dependency.auth import admin_only

faqRouter = APIRouter(
    prefix="/faqs",
    tags=["faqs"]
)

def convert_objectid_to_str(data):
    """Recursively convert ObjectId fields in a dictionary to strings."""
    if isinstance(data, dict):
        return {k: convert_objectid_to_str(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_objectid_to_str(item) for item in data]
    elif isinstance(data, ObjectId):
        return str(data)
    return data

@faqRouter.post("/",response_model=FAQsSchemaReq)
async def create_faq(faq: FAQsSchemaReq):
    """
    Create a new FAQ
    
    Args:
        faq (FAQsSchemaReq): The FAQ data to be created
        
    Returns:
        JSONResponse: Created FAQ data or error message
    """
    try:
        new_faq = await FAQService.createFAQ(faq)
        if new_faq:
            new_faq = convert_objectid_to_str(new_faq)
            response = {
                "status": "success",
                "data": new_faq,
                "message": "FAQ created successfully"
            }
            return JSONResponse(content=response, status_code=status.HTTP_201_CREATED)
        
        response = {
            "status": "failed",
            "message": "Failed to create FAQ"
        }
        return JSONResponse(content=response, status_code=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        response = {
            "status": "error",
            "message": str(e)
        }
        return JSONResponse(content=response, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@faqRouter.get("/", response_model=List[FAQsSchemaReq])
async def get_all_faqs():
    """
    Get all FAQs
    
    Returns:
        JSONResponse: List of FAQs or error message
    """
    try:
        faqs = await FAQService.getAllFAQs()
        if faqs:
            faqs = convert_objectid_to_str(faqs)
            response = {
                "status": "success",
                "data": faqs,
                "message": "FAQs retrieved successfully"
            }
            return JSONResponse(content=response, status_code=status.HTTP_200_OK)
        
        response = {
            "status": "success",
            "data": [],
            "message": "No FAQs found"
        }
        return JSONResponse(content=response, status_code=status.HTTP_200_OK)
        
    except Exception as e:
        response = {
            "status": "error",
            "message": str(e)
        }
        return JSONResponse(content=response, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@faqRouter.get("/{faq_id}", response_model=FAQsSchemaReq)
async def get_faq_by_id(faq_id: str):
    """
    Get a specific FAQ by its ID
    
    Args:
        faq_id (str): The ID of the FAQ to retrieve
        
    Returns:
        JSONResponse: FAQ data or error message
    """
    try:
        faq = await FAQService.getFAQById(faq_id)
        if faq:
            faq = convert_objectid_to_str(faq)
            response = {
                "status": "success",
                "data": faq,
                "message": "FAQ retrieved successfully"
            }
            return JSONResponse(content=response, status_code=status.HTTP_200_OK)
        
        response = {
            "status": "failed",
            "message": "FAQ not found"
        }
        return JSONResponse(content=response, status_code=status.HTTP_404_NOT_FOUND)
        
    except Exception as e:
        response = {
            "status": "error",
            "message": str(e)
        }
        return JSONResponse(content=response, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)