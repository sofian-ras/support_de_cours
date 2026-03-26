from fastapi import APIRouter, HTTPException, status
from app.schemas.auth import UserRegister, UserOut
from app.security import hash_password
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends
from app.security import verify_password, create_access_token
from app.schemas.auth import Token

router = APIRouter(prefix="/auth", tags=["Authentification"])

fake_users_db = []

@router.post("/register", response_model=UserOut)
def register(user_data: UserRegister):
    for u in fake_users_db:
        if u["username"] == user_data.username:
            raise HTTPException(
                status_code=400,
                detail="nom user existe déjà")
        
    hashed_pwd = hash_password(user_data.password)

    new_user = {
        "id": len(fake_users_db) + 1,
        "username": user_data.username,
        "hashed_password": hashed_pwd
    }

    fake_users_db.append(new_user)
    return new_user

@router.post("/token",response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = next((u for u in fake_users_db if u["username"] == form_data.username), None)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="identifiants incorrects")
    
    #verify_password de security.py pour comparer le mot de passe en clair avec le mot de passe hashé
    if not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=400,
            detail="identifiants incorrects")
    
    acccess_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": acccess_token, "token_type": "bearer"}