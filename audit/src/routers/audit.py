from fastapi import APIRouter
from services.auditService import AuditService
from schemas.auditSchema import Audit
from fastapi import HTTPException, status
from typing import List

audit_router = APIRouter()
@audit_router.post("/audits", status_code=status.HTTP_201_CREATED)
async def add_audits(AuditData : Audit):
    response = await AuditService.add_audits(AuditData)
    if not response:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to add audit")
    print(f"Audit added with id: {response}")
    return response

@audit_router.get("/audits", response_model=List[Audit], status_code=status.HTTP_200_OK)
async def get_all_audits() -> List[Audit]:
    audits = await AuditService.get_all_audits()
    if not audits:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No audits found")
    return audits

@audit_router.get("/audits/{audit_id}", response_model=Audit, status_code=status.HTTP_200_OK)
async def get_audit_by_id(audit_id: str) -> Audit:
    audit = await AuditService.get_audit_by_id(audit_id)
    if not audit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Audit not found")
    return audit

@audit_router.get("/audits/user/{user_id}", response_model=List[Audit], status_code=status.HTTP_200_OK)
async def get_audit_by_user_id(user_id: str) -> List[Audit]:
    audits = await AuditService.get_audit_by_user_id(user_id)
    if not audits:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No audits found for this user")
    return audits

@audit_router.get("/audits/action/{action}", response_model=List[Audit], status_code=status.HTTP_200_OK)
async def get_audit_by_action(action: str) -> List[Audit]:
    audits = await AuditService.get_audit_by_action(action)
    if not audits:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No audits found for this action")
    return audits
