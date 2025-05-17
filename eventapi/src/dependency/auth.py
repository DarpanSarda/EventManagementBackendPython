from fastapi import HTTPException , status , Depends , Security
from fastapi.security.api_key import APIKeyHeader
from jose import JWTError, jwt
from utils.jwt_config import SECRET_KEY, ALGORITHM
from repository.user_repo import UserRepo

api_key_header = APIKeyHeader(name="Authorization" , auto_error=True)

async def get_current_user(token: str = Security(api_key_header)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        return email
    except JWTError:
        raise credentials_exception
    

async def admin_only(email : str = Depends(get_current_user)):
    """Ensure the user has admin role"""
    print(f"{email}")
    if email is not None:
        user = UserRepo.findUserByEmail(email=email)
        print(f"{user}")
        if user['role'] != 'admin':
            raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource",
        )
        return user
    raise HTTPException(
        status_code = status.HTTP_404_NOTFOUND,
        detail="User Not Found",
    )