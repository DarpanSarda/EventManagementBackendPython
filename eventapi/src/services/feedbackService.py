from repository.feedback_repo import FeedbackRepo
from schemas.feedbackSchema import FeedbackSchemaReq

class FeedbackService:
    @staticmethod
    async def createFeedback(feedback: FeedbackSchemaReq):
        """
        Create a new feedback
        
        Args:
            feedback (FeedbackSchemaReq): The feedback data to be created
            
        Returns:
            dict: The newly created feedback document
            
        Raises:
            Exception: If there's an error during feedback creation
        """
        try:
            if not feedback:
                raise Exception("Feedback data is required")
                
            new_feedback = await FeedbackRepo.addFeedback(feedback)
            if not new_feedback:
                raise Exception("Failed to create feedback")
                
            return new_feedback
            
        except Exception as e:
            print(f"Error creating feedback: {str(e)}")
            raise Exception(f"Failed to create feedback: {str(e)}")
            
    @staticmethod
    async def getFeedbackForUser(user_id: str):
        """
        Get all feedback for a specific user
        
        Args:
            user_id (str): The ID of the user to get feedback for
            
        Returns:
            list: List of feedback documents if found
            None: If no feedback is found
            
        Raises:
            Exception: If there's an error during feedback retrieval
        """
        try:
            if not user_id:
                raise Exception("User ID is required")
                
            feedbacks = await FeedbackRepo.getFeedbackByUser(user_id)
            if not feedbacks:
                return None
            return feedbacks
            
        except Exception as e:
            print(f"Error retrieving feedback for user: {str(e)}")
            raise Exception(f"Failed to retrieve feedback for user: {str(e)}")
        
    @staticmethod
    async def getFeedbackById(feedback_id: str):
        """
        Get a specific feedback by its ID
            
        Args:
            feedback_id (str): The ID of the feedback to retrieve
                
        Returns:
            dict: The feedback document if found
            None: If feedback is not found
                
        Raises:
            Exception: If there's an error during feedback retrieval
        """
        try:
            if not feedback_id:
                raise Exception("Feedback ID is required")
                    
            feedback = await FeedbackRepo.getFeedbackById(feedback_id)
            if not feedback:
                return None
            return feedback
                
        except Exception as e:
            print(f"Error retrieving feedback: {str(e)}")
            raise Exception(f"Failed to retrieve feedback: {str(e)}")