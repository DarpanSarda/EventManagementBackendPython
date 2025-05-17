from eventapi import APIRouter, status
from fastapi.responses import JSONResponse
from schemas.feedbackSchema import FeedbackSchemaReq
from services.feedbackService import FeedbackService
from bson import ObjectId
from typing import List

feedbackRouter = APIRouter(
    prefix="/feedback",
    tags=["feedback"]
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

@feedbackRouter.post("/", response_model=FeedbackSchemaReq)
async def create_feedback(feedback: FeedbackSchemaReq):
    """
    Create a new feedback
    
    Args:
        feedback (FeedbackSchemaReq): The feedback data to be created
        
    Returns:
        JSONResponse: Created feedback data or error message
    """
    try:
        print(f"routes {feedback}")
        new_feedback = await FeedbackService.createFeedback(feedback)
        if new_feedback:
            new_feedback = convert_objectid_to_str(new_feedback)
            response = {
                "status": "success",
                "data": new_feedback,
                "message": "Feedback created successfully"
            }
            return JSONResponse(content=response, status_code=status.HTTP_201_CREATED)
        
        response = {
            "status": "failed",
            "message": "Failed to create feedback"
        }
        return JSONResponse(content=response, status_code=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        response = {
            "status": "error",
            "message": str(e)
        }
        return JSONResponse(content=response, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@feedbackRouter.get("/user/{user_id}", response_model=List[FeedbackSchemaReq])
async def get_user_feedback(user_id: str):
    """
    Get all feedback for a specific user
    
    Args:
        user_id (str): The ID of the user to get feedback for
        
    Returns:
        JSONResponse: List of feedback or error message
    """
    try:
        feedbacks = await FeedbackService.getFeedbackForUser(user_id)
        if feedbacks:
            feedbacks = convert_objectid_to_str(feedbacks)
            response = {
                "status": "success",
                "data": feedbacks,
                "message": "Feedback retrieved successfully"
            }
            return JSONResponse(content=response, status_code=status.HTTP_200_OK)
        
        response = {
            "status": "success",
            "data": [],
            "message": "No feedback found for this user"
        }
        return JSONResponse(content=response, status_code=status.HTTP_200_OK)
        
    except Exception as e:
        response = {
            "status": "error",
            "message": str(e)
        }
        return JSONResponse(content=response, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@feedbackRouter.get("/{feedback_id}", response_model=FeedbackSchemaReq)
async def get_feedback_by_id(feedback_id: str):
    """
    Get a specific feedback by its ID
    
    Args:
        feedback_id (str): The ID of the feedback to retrieve
        
    Returns:
        JSONResponse: Feedback data or error message
    """
    try:
        feedback = await FeedbackService.getFeedbackById(feedback_id)
        if feedback:
            feedback = convert_objectid_to_str(feedback)
            response = {
                "status": "success",
                "data": feedback,
                "message": "Feedback retrieved successfully"
            }
            return JSONResponse(content=response, status_code=status.HTTP_200_OK)
        
        response = {
            "status": "failed",
            "message": "Feedback not found"
        }
        return JSONResponse(content=response, status_code=status.HTTP_404_NOT_FOUND)
        
    except Exception as e:
        response = {
            "status": "error",
            "message": str(e)
        }
        return JSONResponse(content=response, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

