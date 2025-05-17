from repository.user_repo import UserRepo
from schemas.authentication import RegistrationReq , LoginReq
import bcrypt

class UserService:
    @staticmethod
    def RegisterUser(user : RegistrationReq):
        """Register a user after checking if email is not exists"""
        ifUserPresent = UserRepo.findUserByEmail(user.email)
        if ifUserPresent:
            return{
                "error":"User Already Exists"
            }

        print("service " , user)

        hash_password =  bcrypt.hashpw(user.password.encode('utf-8') , bcrypt.gensalt())
        user.password = hash_password.decode('utf-8')
        newUser =UserRepo.insertUser(user)
        return{
            "name": newUser["name"],
            "lastname": newUser["lastname"],
            "email": newUser["email"],
            "role": newUser["role"],
            "isVerified": newUser["isVerified"],
            "message": "User registered successfully!"
        }
    
    @staticmethod
    def LoginUser(user : LoginReq):
        """Login a user by checking email exists"""
        ifUserPresent = UserRepo.findUserByEmail(user.email)
        if ifUserPresent is None:
            return{
                "error":"Please Logon First"
            }
        print("service login " , ifUserPresent)
        return{
            "messge":"Login success",
            "_id":ifUserPresent["_id"],
            "email":ifUserPresent["email"],
            "password":ifUserPresent["password"]
        }
    
    @staticmethod
    def GetUserByEmail(email : str):
        """Get user by email"""
        user = UserRepo.findUserByEmail(email)
        if user is None:
            return{
                "error":"User not found"
            }
        return{
            "name": user["name"],
            "email": user["email"],
            "avatar": user["avatar"],
            "_id": user["_id"]
        }
    
    @staticmethod
    async def GetAllUsers():
        """
        Get all users from the database
        """
        users = await UserRepo.getAllUsers()
        if users is None:
            return{
                "error":"No users found"
            }
        return users