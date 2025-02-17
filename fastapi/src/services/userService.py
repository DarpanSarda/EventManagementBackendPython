from repository.user_repo import UserRepo
from models.users import Users
import bcrypt

class UserService:
    @staticmethod
    def RegisterUser(user : Users):
        """Register a user after checking if email is not exists"""

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
