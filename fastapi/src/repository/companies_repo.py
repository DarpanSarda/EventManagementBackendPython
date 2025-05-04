from db.connect import MongoDBSingleton
from bson import ObjectId
from schemas.companiesSchema import CompaniesAdmin

db = MongoDBSingleton().get_database()
if db is not None:
    companies_collection = db["clients"]
else:
    companies__collection = None

class CompanyRepo():
    @staticmethod
    async def getAllCompanies():
        """
        Get all companies from the database
        
        Returns:
            list: List of company documents if found, empty list if not found
            
        Raises:
            Exception: If there's an error during the database operation
        """
        try:
            if companies_collection is None:
                raise Exception("Database connection failed")
                
            print("Inside findcompanies")
            companies_cursor = companies_collection.find({}, {'_id': 0})
            companies = []
            for company in companies_cursor:
                companies.append(company)
            print(f"companies repo {companies}")
            return companies
            
        except Exception as e:
            print(f"Error retrieving companies: {str(e)}")
            raise Exception(f"Failed to retrieve companies: {str(e)}")
    
    @staticmethod
    async def addCompany(company_data: CompaniesAdmin):
        """
        Add a new company to the database
        
        Args:
            company_data (CompaniesAdmin): The company data to be added
            
        Returns:
            dict: The newly created company document with _id
            
        Raises:
            Exception: If there's an error during the database operation
        """
        try:
            if companies_collection is None:
                raise Exception("Database connection failed")
                
            # Validate company data
            if not company_data:
                raise Exception("Company data is required")
                
            # Convert Pydantic model to dict
            company_dict = company_data.model_dump()
            
            # Insert the company
            result = companies_collection.insert_one(company_dict)
            print(result)
            if result.inserted_id:
                # Fetch and return the newly created company
                new_company = companies_collection.find_one(
                    {"_id": result.inserted_id}
                )
                return new_company
            else:
                raise Exception("Failed to insert company")
                
        except Exception as e:
            print(f"Error adding company: {str(e)}")
            raise Exception(f"Failed to add company: {str(e)}")
