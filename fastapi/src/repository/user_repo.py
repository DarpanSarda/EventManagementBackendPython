from db.connect import connect_database
from models import users

db = connect_database()
if db is not None:
    database = db["eventManagement"]
    user_collection = database["users"]
else:
    user_collection = None
class UserRepo():
    @staticmethod
    def insertUser(userData : users)->dict:
        """To insert the user in the db"""
        print("repository " , userData)
        if user_collection is None:
            raise Exception("Database connection failed")
        new_user = {
            "name" : userData.name,
            "lastname" : userData.lastname,
            "email" : userData.email,
            "avatar" : userData.avatar or "",
            "password" : userData.password,
            "otp" : userData.otp or 0,
            "role" : userData.role or "user",
            "isVerified" : userData.isVerified or False,
        }
        returned_user = user_collection.insert_one(new_user)
        print("repo response" , returned_user)
        return new_user