from db.connect import MongoDBSingleton
from schemas.auditSchema import Audit
from bson import ObjectId

db = MongoDBSingleton().get_database()
if db is not None:
    audit_collection = db["audit"]
else:
    audit_collection = None
    raise Exception("Failed to connect to MongoDB")

class AuditRepository:

    @staticmethod
    async def get_all_audits() -> list:
        """
        Retrieve all audit records from the database.
        Returns:
            list: A list of audit records.
        Raises:
            Exception: If the database connection fails.
        """
        try:
            audits_cursor = audit_collection.find({}, {'_id': 0})
            audits = []
            for audit in audits_cursor:
                audits.append(audit)
            return audits
        except Exception as e:
            raise Exception(f"Failed to retrieve all audits: {e}")
    
    @staticmethod
    async def add_audits(AuditData : Audit) -> bool:
        """
        Add a new audit record to the database.
        Returns:
            bool: True if the audit was added successfully, False otherwise.
        Raises:
            Exception: If the database connection fails.
        """
        try:
            audit = audit_collection.insert_one(AuditData.model_dump())
            print(f"Audit added with id: {audit}")
            if audit:
                print(f"Audit added with id: {audit.inserted_id}")
            else:
                print("Failed to add audit")
                return False
            return True
        except Exception as e:
            raise Exception(f"Failed to add audit: {e}")
    
    @staticmethod
    async def get_audit_by_id(audit_id: str) -> Audit:
        """
        Retrieve an audit record by its ID.
        Args:
            audit_id (str): The ID of the audit record to retrieve.
        Returns:
            Audit: The audit record with the specified ID.
        Raises:
            Exception: If the database connection fails.
        """
        try:
            audit_object_id = ObjectId(audit_id)
            audit = audit_collection.find_one({"_id": audit_object_id})
            if audit:
                return Audit(**audit)
            else:
                raise Exception("Audit not found")
        except Exception as e:
            raise Exception(f"Failed to retrieve audit by ID: {e}")
        
    @staticmethod
    async def get_audit_by_user_id(user_id: str) -> list:
        """
        Retrieve audit records by user ID.
        Args:
            user_id (str): The user ID to filter audits by.
        Returns:
            list: A list of audit records associated with the specified user ID.
        Raises:
            Exception: If the database connection fails.
        """
        try:
            audits_cursor = audit_collection.find({"userId": user_id}, {'_id': 0})
            audits = []
            for audit in audits_cursor:
                audits.append(audit)
            return audits
        except Exception as e:
            raise Exception(f"Failed to retrieve audits by user ID: {e}")
    
    @staticmethod
    async def get_audit_by_action(action: str) -> list:
        """
        Retrieve audit records by action type.
        Args:
            action (str): The action type to filter audits by.
        Returns:
            list: A list of audit records associated with the specified action type.
        Raises:
            Exception: If the database connection fails.
        """
        try:
            audits_cursor = audit_collection.find({"action": action}, {'_id': 0})
            audits = []
            for audit in audits_cursor:
                audits.append(audit)
            return audits
        except Exception as e:
            raise Exception(f"Failed to retrieve audits by action: {e}")