from repository.faqs_repo import FAQsRepo
from schemas.faqsSchema import FAQsSchemaReq
from typing import List, Optional

class FAQService:
    @staticmethod
    async def createFAQ(faq: FAQsSchemaReq):
        """
        Create a new FAQ
        
        Args:
            faq (FAQsSchemaReq): The FAQ data to be created
            
        Returns:
            dict: The newly created FAQ document
            
        Raises:
            Exception: If there's an error during FAQ creation
        """
        try:
            if not faq:
                raise Exception("FAQ data is required")
                
            new_faq = await FAQsRepo.addFAQ(faq)
            if not new_faq:
                raise Exception("Failed to create FAQ")
                
            return new_faq
            
        except Exception as e:
            print(f"Error creating FAQ: {str(e)}")
            raise Exception(f"Failed to create FAQ: {str(e)}")
    
    @staticmethod
    async def getAllFAQs() -> List[dict]:
        """
        Get all FAQs
        
        Returns:
            List[dict]: List of FAQ documents
            None: If no FAQs are found
            
        Raises:
            Exception: If there's an error during FAQ retrieval
        """
        try:
            faqs = await FAQsRepo.getAllFAQs()
            if not faqs:
                return None
            return faqs
            
        except Exception as e:
            print(f"Error retrieving FAQs: {str(e)}")
            raise Exception(f"Failed to retrieve FAQs: {str(e)}")
    
    @staticmethod
    async def getFAQById(faq_id: str) -> Optional[dict]:
        """
        Get a specific FAQ by its ID
        
        Args:
            faq_id (str): The ID of the FAQ to retrieve
            
        Returns:
            Optional[dict]: The FAQ document if found
            None: If FAQ is not found
            
        Raises:
            Exception: If there's an error during FAQ retrieval
        """
        try:
            if not faq_id:
                raise Exception("FAQ ID is required")
                
            faq = await FAQsRepo.getFAQById(faq_id)
            if not faq:
                return None
            return faq
            
        except Exception as e:
            print(f"Error retrieving FAQ: {str(e)}")
            raise Exception(f"Failed to retrieve FAQ: {str(e)}")