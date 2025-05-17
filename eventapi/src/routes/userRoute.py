from fastapi import APIRouter , HTTPException , Depends , status
from fastapi.responses import JSONResponse
from schemas.userSchema import UserProfileRes 
from services.userService import UserService
from pydantic import EmailStr 
from typing import Annotated
from dependency.auth import get_current_user

userRouter = APIRouter(
    tags=["User"],
    prefix="/user"
)

@userRouter.get("/profile", response_model=UserProfileRes)
async def get_user_profile(current_user: Annotated[str, Depends(get_current_user)]):
    """
    Get the profile of the currently authenticated user based on their JWT token.
    The token is automatically extracted and validated by the get_current_user dependency.
    """
    try:
        # Get user details from the email extracted from the token
        response = UserService.GetUserByEmail(email=current_user)
        
        if "error" in response:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=response["error"]
            )
        
        # Return the user profile data with required message field
        return UserProfileRes(
            name=response["name"],
            email=response["email"],
            avatar=response.get("avatar"),  # Using get() to handle None safely
            message="Profile retrieved successfully"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve user profile: {str(e)}"
        )
    
@userRouter.get("/")
async def get_all_users():
    """
    Get a list of all users.
    """
    try:
        # Get all users from the database
        response = await UserService.GetAllUsers()
        for res in response:
            res['_id'] = str(res['_id'])
        if "error" in response:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=response["error"]
            )
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve users: {str(e)}"
        )