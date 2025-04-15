from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from utils.auth_utils import create_access_token, decode_token

router = APIRouter(prefix="/protected", tags=["Secure"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

@router.get("/me")
def secure_area(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_id = payload.get("sub")
    device_token = payload.get("device_token")
    if not device_token:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    refreshed_token = create_access_token(
        data={"sub": user_id, "device_token": device_token},
        expires_delta=timedelta(minutes=30)
    )
    
    return {
        "message": "Secure area", 
        "user_id": user_id, 
        "device_token": device_token, 
        "refreshed_access_token": refreshed_token}

