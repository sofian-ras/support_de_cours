from pydantic import BaseModel, Field, ConfigDict, field_validator
import re

# Ce qu'on reçoit lors d'une inscription
class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    password: str = Field(..., min_length=8, max_length=72)

    # logique de validation du fichier
    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        if not re.search(r"[A-Z]", v):
            raise ValueError("le mot de passe doit contenir au moins une majuscule")
        if not re.search(r"\d", v):
            raise ValueError("le mot de passe doit contenir au moins un chiffre")
        return v

# on cache le mot de passe
class UserOut(BaseModel):
    id: int
    username: str
    
    model_config = ConfigDict(from_attributes=True)

# Le format du badge
class Token(BaseModel):
    access_token: str
    token_type: str