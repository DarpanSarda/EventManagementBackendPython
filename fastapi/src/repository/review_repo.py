from db.connect import MongoDBSingleton
from bson import ObjectId
from schemas.reviewSchema import ReviewSchemaReq

db = MongoDBSingleton().get_database()
if db is not None:
    review_collection = db["reviews"]
else:
    review_collection = None

class ReviewRepo():

    @staticmethod
    async def addReview(review: ReviewSchemaReq):
        """
        Create a new review in the database
        
        Args:
            review (ReviewSchemaReq): The review data to be added
            
        Returns:
            dict: The newly created review document
            
        Raises:
            Exception: If there's an error during the database operation
        """
        try:
            if review_collection is None:
                raise Exception("Database connection failed")
                
            if not review:
                raise Exception("Review data is required")
                
            # Convert Pydantic model to dict
            review_dict = review.model_dump(exclude={'id'})
            
            # Insert the review
            result = review_collection.insert_one(review_dict)
            
            if result.inserted_id:
                # Fetch and return the newly created review
                new_review = review_collection.find_one(
                    {"_id": result.inserted_id}
                )
                return new_review
            else:
                raise Exception("Failed to insert review")
                
        except Exception as e:
            print(f"Error adding review: {str(e)}")
            raise Exception(f"Failed to add review: {str(e)}")
        
    @staticmethod
    async def getReviewByEvent(event: ObjectId):
        """
        Get all reviews for a specific event
        
        Args:
            event (ObjectId): The ID of the event to get reviews for
            
        Returns:
            list: List of review documents if found, empty list if not found
            
        Raises:
            Exception: If there's an error during the database operation
        """
        try:
            if review_collection is None:
                raise Exception("Database connection failed")
                
            if not ObjectId.is_valid(event):
                raise Exception("Invalid event ID format")
                
            cursor = review_collection.find({"event": event})
            print(cursor)
            reviews = cursor.to_list(length=None)
            print(reviews)
            return reviews
            
        except Exception as e:
            print(f"Error retrieving reviews: {str(e)}")
            raise Exception(f"Failed to retrieve reviews: {str(e)}")    

    @staticmethod
    async def getReviewByUser(user: ObjectId):
        """
        Get all reviews for a specific user
        
        Args:
            user (ObjectId): The ID of the user to get reviews for
            
        Returns:
            list: List of review documents if found, empty list if not found
            
        Raises:
            Exception: If there's an error during the database operation
        """
        try:
            print(f"user {user} {type(user)}")
            if review_collection is None:
                raise Exception("Database connection failed")
                
            if not ObjectId.is_valid(user):
                raise Exception("Invalid user ID format")
                
            cursor = review_collection.find({"user": str(user)})
            reviews = cursor.to_list(length=None)
            print(f"reviews {reviews}")
            return reviews
            
        except Exception as e:
            print(f"Error retrieving reviews: {str(e)}")
            raise Exception(f"Failed to retrieve reviews: {str(e)}")            
    