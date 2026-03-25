import uvicorn
from fastapi import FastAPI, status
from pydantic import BaseModel, model_validator

app = FastAPI()


class Password(BaseModel):
    password: str
    confirm_password: str

    @model_validator(mode="after")
    def check_password(self):
        p = self.password
        if len(p) < 8:
            raise ValueError("password too short")
        if not any(c.islower() for c in p):
            raise ValueError("password must contain a lowercase letter")
        if not any(c.isupper() for c in p):
            raise ValueError("password must contain an uppercase letter")
        if not any(c.isdigit() for c in p):
            raise ValueError("password must contain a digit")
        if not any(not c.isalnum() for c in p):
            raise ValueError("password must contain a symbol")
        if self.confirm_password != p:
            raise ValueError("passwords do not match")
        return self


@app.post("/passwords", status_code=status.HTTP_201_CREATED)
def validate_password(payload: Password):
    return {"message": "Password is valid"}


if __name__ == "__main__":
    uvicorn.run("exo2:app", host="127.0.0.1", port=8001, reload=True)
