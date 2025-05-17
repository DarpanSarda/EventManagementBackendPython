from fastapi import APIRouter, status , Depends
from fastapi.responses import JSONResponse
from schemas.reviewSchema import ReviewSchemaReq , PyObjectId
from services.reviewService import ReviewService
from bson import ObjectId
from typing import List 

reviewRouter = APIRouter(
    prefix="/review",
    tags=["review","rating"],
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

@reviewRouter.post("/", response_model=ReviewSchemaReq)
async def create_review(review: ReviewSchemaReq):
    """
    Create a new review
    
    Args:
        review (ReviewSchemaReq): The review data to be created
        
    Returns:
        JSONResponse: Created review data or error message
    """
    try:
        # review_dict = review.model_dump()
        new_review = await ReviewService.createReview(review)
        
        if new_review:
            new_review = convert_objectid_to_str(new_review)  # Convert ObjectId to string
            response = {
                "status": "success",
                "data": new_review,
                "message": "Review created successfully"
            }
            return JSONResponse(content=response, status_code=status.HTTP_201_CREATED)
        
        response = {
            "status": "failed",
            "message": "Failed to create review"
        }
        return JSONResponse(content=response, status_code=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        response = {
            "status": "error",
            "message": str(e)
        }
        return JSONResponse(content=response, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@reviewRouter.get("/event/{event_id}", response_model=List[ReviewSchemaReq])
async def get_reviews_by_event(event_id: PyObjectId):
    """
    Get all reviews for a specific event
    
    Args:
        event_id (PyObjectId): The ID of the event to get reviews for
        
    Returns:
        JSONResponse: List of reviews or error message
    """
    try:
        reviews = await ReviewService.getReviewForEvent(event_id)
        if reviews:
            reviews = convert_objectid_to_str(reviews)
            response = {
                "status": "success",
                "data": reviews,
                "message": "Reviews retrieved successfully"
            }
            return JSONResponse(content=response, status_code=status.HTTP_200_OK)
        
        response = {
            "status": "success",
            "data": [],
            "message": "No reviews found for this event"
        }
        return JSONResponse(content=response, status_code=status.HTTP_200_OK)
        
    except Exception as e:
        response = {
            "status": "error",
            "message": str(e)
        }
        return JSONResponse(content=response, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@reviewRouter.get("/user", response_model=List[ReviewSchemaReq])
async def get_reviews_by_user(email: str):
    """
    Get all reviews by a specific user
    
    Args:
        email (str): The email of the user to get reviews for
        
    Returns:
        JSONResponse: List of reviews or error message
    """
    try:
        if not email:
            response = {
                "status": "failed",
                "message": "Email is required"
            }
            return JSONResponse(content=response, status_code=status.HTTP_400_BAD_REQUEST)
            
        reviews = await ReviewService.getReviewForUser(email)
        if reviews:
            reviews = convert_objectid_to_str(reviews)
            response = {
                "status": "success",
                "data": reviews,
                "message": "Reviews retrieved successfully"
            }
            return JSONResponse(content=response, status_code=status.HTTP_200_OK)
        
        response = {
            "status": "success",
            "data": [],
            "message": "No reviews found for this user"
        }
        return JSONResponse(content=response, status_code=status.HTTP_200_OK)
        
    except Exception as e:
        response = {
            "status": "error",
            "message": str(e)
        }
        return JSONResponse(content=response, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)