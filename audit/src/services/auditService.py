from repository.audit_repo import AuditRepository
from schemas.auditSchema import Audit

class AuditService:
    @staticmethod
    async def add_audits(AuditData : Audit):
        """
        Add a new audit record to the database.
        Args:
            AuditData (Audit): The audit data to be added.      
        """
        response = await AuditRepository.add_audits(AuditData)
        print(f"Audit added with id: {response}")
        return response
    @staticmethod
    async def get_all_audits() -> list:
        return await AuditRepository.get_all_audits()
    @staticmethod
    async def get_audit_by_id(audit_id: str) -> Audit:
        return await AuditRepository.get_audit_by_id(audit_id)
    @staticmethod
    async def get_audit_by_user_id(user_id: str) -> list:
        return await AuditRepository.get_audit_by_user_id(user_id)
    @staticmethod
    async def get_audit_by_action(action: str) -> list:
        return await AuditRepository.get_audit_by_action(action)