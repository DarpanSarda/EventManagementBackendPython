from fastapi import APIRouter , HTTPException
from schemas.authentication import RegistrationReq , RegistrationRes 
from services.userService import UserService

authRouter = APIRouter(
    tags=["auth"],
    prefix="/auth"
)

@authRouter.post("/register" , response_model=RegistrationRes)
def user_register(user : RegistrationReq):
    print("router : " , user)
    response = UserService.RegisterUser(user)
    print("auth route register " , response)
    if "error" in response:
        raise HTTPException(status_code = 400 , detail = response["error"])

    return{
        "name" : response["name"],
        "email" : response["email"],
        "message" : "User Registered Sucessfully"
    }