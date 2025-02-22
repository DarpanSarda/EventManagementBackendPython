from fastapi import APIRouter , HTTPException , Depends
from fastapi.responses import JSONResponse
from schemas.userSchema import UserProfileRes 
from services.userService import UserService
from pydantic import EmailStr
from dependency.auth import get_current_user

userRouter = APIRouter(
    tags=["User"],
    prefix="/user"
)

@userRouter.get("/profile" , response_model = UserProfileRes)
def get_user(email : str = Depends(get_current_user)):
    response = UserService.GetUserByEmail(email=email)
    if "error" in response:
        return JSONResponse(status_code=400, content={"error": response["error"]})
    
    return JSONResponse(
        status_code=200,
        content = {
        "name" : response["name"],
        "email" : response["email"],
        "avatar" : response["avatar"]
    })