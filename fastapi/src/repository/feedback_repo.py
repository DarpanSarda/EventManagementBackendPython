from db.connect import MongoDBSingleton
from bson import ObjectId
from schemas.feedbackSchema import FeedbackSchemaReq
from pymongo.errors import PyMongoError
from typing import List, Optional

db = MongoDBSingleton().get_database()
if db is not None:
    feedback_collection = db["feedback"]
else:
    feedback_collection = None

class FeedbackRepo():
    @staticmethod
    async def addFeedback(feedback: FeedbackSchemaReq):
        """
        Add a new feedback to the database
        
        Args:
            feedback (FeedbackSchemaReq): The feedback data to be added
    
        Returns:
            dict: The newly created feedback document with _id
            
        Raises:
            PyMongoError: If there's an error during database operation
            Exception: For any other unexpected errors
        """
        try:
            if feedback_collection is None:
                raise Exception("Database connection not established")
                
            # Convert Pydantic model to dict excluding any None values
            feedback_dict = feedback.model_dump(exclude_none=True, exclude={'id'})
            
            # Insert the feedback
            result = feedback_collection.insert_one(feedback_dict)
            
            if result.inserted_id:
                # Fetch and return the newly created feedback
                new_feedback = feedback_collection.find_one(
                    {"_id": result.inserted_id}
                )
                return new_feedback
            else:
                raise Exception("Failed to insert feedback")
                
        except PyMongoError as e:
            print(f"Database error occurred: {str(e)}")
            raise Exception(f"Database error occurred: {str(e)}")
        except Exception as e:
            print(f"Error adding feedback: {str(e)}")
            raise Exception(f"Error adding feedback: {str(e)}")

    @staticmethod
    async def getFeedbackByUser(user_id: str) -> List[dict]:
        """
        Get all feedback for a specific user
        
        Args:
            user_id (str): The ID of the user to get feedback for
            
        Returns:
            List[dict]: List of feedback documents if found
            
        Raises:
            PyMongoError: If there's an error during database operation
            Exception: For any other unexpected errors
        """
        try:
            if feedback_collection is None:
                raise Exception("Database connection not established")

            if not ObjectId.is_valid(user_id):
                raise Exception("Invalid user ID format")
            
            # Use await with the find operation
            cursor = feedback_collection.find({"user": user_id}).to_list(None)
            return cursor if cursor else []
            
        except PyMongoError as e:
            print(f"Database error occurred: {str(e)}")
            raise Exception(f"Database error occurred: {str(e)}")
        except Exception as e:
            print(f"Error retrieving feedback: {str(e)}")
            raise Exception(f"Error retrieving feedback: {str(e)}")
        
    @staticmethod
    async def getFeedbackById(feedback_id: str) -> Optional[dict]:
        """
        Get a specific feedback by its ID
        
        Args:
            feedback_id (str): The ID of the feedback to retrieve
            
        Returns:
            Optional[dict]: The feedback document if found, None otherwise
            
        Raises:
            PyMongoError: If there's an error during database operation
            Exception: For any other unexpected errors
        """
        try:
            if feedback_collection is None:
                raise Exception("Database connection not established")
    
            if not ObjectId.is_valid(feedback_id):
                raise Exception("Invalid feedback ID format")
                
            feedback = feedback_collection.find_one({"_id": ObjectId(feedback_id)})
            return feedback
            
        except PyMongoError as e:
            print(f"Database error occurred: {str(e)}")
            raise Exception(f"Database error occurred: {str(e)}")
        except Exception as e:
            print(f"Error retrieving feedback: {str(e)}")
            raise Exception(f"Error retrieving feedback: {str(e)}")