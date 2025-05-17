from repository.review_repo import ReviewRepo
from schemas.reviewSchema import ReviewSchemaReq
from bson import ObjectId
from services.userService import UserService

class ReviewService:

    @staticmethod
    async def createReview(review: ReviewSchemaReq):
        """
        Create a new review
                
        Args:
            review (ReviewSchemaReq): The review data to be created
                    
        Returns:
            dict: The newly created review document
                    
        Raises:
            Exception: If there's an error during review creation
        """
        try:
            if not review:
                raise Exception("Review data is required")
                        
            returned_review = await ReviewRepo.addReview(review)
            if not returned_review:
                raise Exception("Failed to create review")
                        
            return returned_review
                    
        except Exception as e:
            print(f"Error creating review: {str(e)}")
            raise Exception(f"Failed to create review: {str(e)}")
    
    @staticmethod
    async def getReviewForEvent(event: ObjectId):
        """
        Get all reviews for a specific event
        
        Args:
            event (ObjectId): The ID of the event to get reviews for
            
        Returns:
            list: List of review documents if found
            None: If no reviews are found
            
        Raises:
            Exception: If there's an error during the database operation
        """
        try:
            if not ObjectId.is_valid(event):
                raise Exception("Invalid event ID format")
                
            reviews = await ReviewRepo.getReviewByEvent(event)
            if not reviews:
                return None
            return reviews
            
        except Exception as e:
            print(f"Error retrieving reviews for event: {str(e)}")
            raise Exception(f"Failed to retrieve reviews for event: {str(e)}")
    
    @staticmethod
    async def getReviewForUser(email: str):
        """
        Get all reviews for a specific user
        
        Args:
            email (str): The email of the user to get reviews for
            
        Returns:
            list: List of review documents if found
            None: If no reviews are found
            
        Raises:
            Exception: If there's an error during the database operation
        """
        try:
            if not email:
                raise Exception("Email is required")
                
            print("hw")
            # First get the user ID from the email
            user = UserService.GetUserByEmail(email)
            print(f"user {user}")
            if not user:
                raise Exception("User not found")
                
            user_id = user['_id']
            print(f"user id {user_id} {type(user_id)}")
            if not user_id:
                raise Exception("User ID not found")
                
            # Get reviews for the user
            reviews = await ReviewRepo.getReviewByUser(user_id)
            print(f"reviews {reviews}")
            if not reviews:
                return None
            return reviews
            
        except Exception as e:
            print(f"Error retrieving reviews for user: {str(e)}")
            raise Exception(f"Failed to retrieve reviews for user: {str(e)}")