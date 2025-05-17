from db.connect import MongoDBSingleton
from bson import ObjectId
from schemas.faqsSchema import FAQsSchemaReq
from pymongo.errors import PyMongoError
from typing import List, Optional

db = MongoDBSingleton().get_database()
if db is not None:
    faqs_collection = db["faqs"]
else:
    faqs_collection = None

class FAQsRepo:
    @staticmethod
    async def addFAQ(faq: FAQsSchemaReq):
        """
        Add a new FAQ to the database
        
        Args:
            faq (FAQsSchemaReq): The FAQ data to be added
            
        Returns:
            dict: The newly created FAQ document with _id
            
        Raises:
            PyMongoError: If there's an error during database operation
            Exception: For any other unexpected errors
        """
        try:
            if faqs_collection is None:
                raise Exception("Database connection not established")
                
            faq_dict = faq.model_dump(exclude_none=True, exclude={'id'})
            result = faqs_collection.insert_one(faq_dict)
            
            if result.inserted_id:
                new_faq = faqs_collection.find_one({"_id": result.inserted_id})
                return new_faq
            else:
                raise Exception("Failed to insert FAQ")
                
        except PyMongoError as e:
            print(f"Database error occurred: {str(e)}")
            raise Exception(f"Database error occurred: {str(e)}")
        except Exception as e:
            print(f"Error adding FAQ: {str(e)}")
            raise Exception(f"Error adding FAQ: {str(e)}")

    @staticmethod
    async def getAllFAQs() -> List[dict]:
        """
        Get all FAQs from the database
        
        Returns:
            List[dict]: List of FAQ documents
            
        Raises:
            PyMongoError: If there's an error during database operation
            Exception: For any other unexpected errors
        """
        try:
            if faqs_collection is None:
                raise Exception("Database connection not established")
                
            cursor = faqs_collection.find({})
            faqs = cursor.to_list(length=None)
            return faqs
            
        except PyMongoError as e:
            print(f"Database error occurred: {str(e)}")
            raise Exception(f"Database error occurred: {str(e)}")
        except Exception as e:
            print(f"Error retrieving FAQs: {str(e)}")
            raise Exception(f"Error retrieving FAQs: {str(e)}")

    @staticmethod
    async def getFAQById(faq_id: str) -> Optional[dict]:
        """
        Get a specific FAQ by its ID
        
        Args:
            faq_id (str): The ID of the FAQ to retrieve
            
        Returns:
            Optional[dict]: The FAQ document if found, None otherwise
            
        Raises:
            PyMongoError: If there's an error during database operation
            Exception: For any other unexpected errors
        """
        try:
            if faqs_collection is None:
                raise Exception("Database connection not established")

            if not ObjectId.is_valid(faq_id):
                raise Exception("Invalid FAQ ID format")
                
            faq = faqs_collection.find_one({"_id": ObjectId(faq_id)})
            return faq
            
        except PyMongoError as e:
            print(f"Database error occurred: {str(e)}")
            raise Exception(f"Database error occurred: {str(e)}")
        except Exception as e:
            print(f"Error retrieving FAQ: {str(e)}")
            raise Exception(f"Error retrieving FAQ: {str(e)}")