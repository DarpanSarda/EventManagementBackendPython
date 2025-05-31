from db.connect import MongoDBSingleton
from bson import ObjectId
from schemas.companiesSchema import CompaniesAdmin
from typing import List, Optional

db = MongoDBSingleton().get_database()
if db is not None:
    print("dcd", {db.client})
    companies_collection = db["clients"]
else:
    companies_collection = None

class CompanyRepo():
    @staticmethod
    async def getAllCompanies() -> List[dict]:
        """
        Get all companies from the database using Motor
        
        Returns:
            List[dict]: List of company documents if found, empty list if not found
            
        Raises:
            Exception: If there's an error during the database operation
        """
        try:
            if companies_collection is None:
                raise Exception("Database connection failed")
                
            # print("Inside findcompanies")
            companies_cursor = companies_collection.find({}, {'_id': 0})
            companies = []
            for company in companies_cursor:
                companies.append(company)
            # print(f"companies repo {companies}")
            return companies
            
        except Exception as e:
            print(f"Error retrieving companies: {str(e)}")
            raise Exception(f"Failed to retrieve companies: {str(e)}")
    
    @staticmethod
    async def addCompany(company_data: CompaniesAdmin) -> Optional[dict]:
        """
        Add a new company to the database using Motor
        
        Args:
            company_data (CompaniesAdmin): The company data to be added
            
        Returns:
            Optional[dict]: The newly created company document with _id
            
        Raises:
            Exception: If there's an error during the database operation
        """
        try:
            if companies_collection is None:
                raise Exception("Database connection failed")
                
            if not company_data:
                raise Exception("Company data is required")
                
            # Convert Pydantic model to dict
            company_dict = company_data.model_dump(exclude_unset=True)
            
            # Use Motor's async insert_one
            result = await companies_collection.insert_one(company_dict)
            
            if result.inserted_id:
                # Use Motor's async find_one to get the new document
                new_company = await companies_collection.find_one(
                    {"_id": result.inserted_id}
                )
                if new_company:
                    new_company['_id'] = str(new_company['_id'])
                return new_company
            
            raise Exception("Failed to insert company")
                
        except Exception as e:
            print(f"Error adding company: {str(e)}")
            raise Exception(f"Failed to add company: {str(e)}")
