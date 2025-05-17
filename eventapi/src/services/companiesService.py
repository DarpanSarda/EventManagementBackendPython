from repository.companies_repo import CompanyRepo
from schemas.companiesSchema import CompaniesAdmin

from repository.companies_repo import CompanyRepo
from schemas.companiesSchema import CompaniesAdmin

class CompaniesService:
    @staticmethod
    async def getCompanies():
        """
        Get all companies from the database
        
        Returns:
            list: List of company documents if found
            
        Raises:
            Exception: If there's an error during the database operation
        """
        try:
            companies = await CompanyRepo.getAllCompanies()
            if not companies:
                return []
            return companies
            
        except Exception as e:
            print(f"Error retrieving companies: {str(e)}")
            raise Exception(f"Failed to retrieve companies: {str(e)}")
    
    @staticmethod
    async def AddCompany(company: CompaniesAdmin):
        """
        Add a new company to the database
        
        Args:
            company (CompaniesAdmin): The company data to be added
            
        Returns:
            dict: The newly created company document
            
        Raises:
            Exception: If there's an error during the database operation
        """
        try:
            if not company:
                raise Exception("Company data is required")
                
            returned_company = await CompanyRepo.addCompany(company_data=company)
            if not returned_company:
                raise Exception("Failed to add company")
                
            return returned_company
            
        except Exception as e:
            print(f"Error adding company: {str(e)}")
            raise Exception(f"Failed to add company: {str(e)}")