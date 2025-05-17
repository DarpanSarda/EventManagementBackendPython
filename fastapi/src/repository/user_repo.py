from db.connect import MongoDBSingleton
from models import users
from schemas.authentication import RegistrationReq

db = MongoDBSingleton().get_database()

if db is not None:
    user_collection = db["users"]
else:
    user_collection = None
class UserRepo():

    @staticmethod
    def findUserByEmail(email : str):
        returnedUser = user_collection.find_one({"email" : email})
        return returnedUser

    @staticmethod
    def insertUser(userData : RegistrationReq)->dict:
        """To insert the user in the db"""
        print("repository " , userData)
        if user_collection is None:
            raise Exception("Database connection failed")
        new_user = {
            "name": userData.name,
            "lastname": userData.lastname,
            "email": userData.email,
            "password": userData.password,
            "avatar": userData.avatar if userData.avatar is not None else "",
            "otp": userData.otp if userData.otp is not None else 0,
            "role": userData.role if userData.role is not None else "user",
            "isVerified": userData.isVerified if userData.isVerified is not None else False,
        }
        returned_user = user_collection.insert_one(new_user)
        print("repo response" , returned_user)
        return new_user
    
    @staticmethod
    async def getAllUsers():
        """
        Get all users from the database
        """
        if user_collection is None:
            raise Exception("Database connection failed")
        users_collection = user_collection.find()
        users = []
        for user in users_collection:
            users.append(user)
        return users