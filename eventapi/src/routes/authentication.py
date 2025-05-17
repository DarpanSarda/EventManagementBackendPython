from eventapi import APIRouter , HTTPException
from schemas.authentication import RegistrationReq , RegistrationRes , LoginReq , LoginRes 
from services.userService import UserService
from utils.jwt_config import create_access_token


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

    access_token = create_access_token(data={"sub": user.email})
    return{
        "name" : response["name"],
        "email" : response["email"],
        "token" : access_token,
        "tokenType" : "bearer",
        "message" : "User Registered Sucessfully"
    }

@authRouter.post("/login" , response_model = LoginRes)
def login_user(user : LoginReq):
    print("router login" , user)

    response = UserService.LoginUser(user)
    print(f"response : {response}")
    if "error" in response:
        raise HTTPException(status_code = 400 , detail = response["error"])
    
    access_token = create_access_token(data={"sub": user.email})

    return{
        "id" : str(response["_id"]),
        "email" : response["email"],
        "token" : access_token,
        "tokenType" : "bearer",
        "message" : "User LoggedIn Sucessfully"
    }