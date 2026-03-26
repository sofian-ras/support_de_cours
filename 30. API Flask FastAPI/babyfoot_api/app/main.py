from fastapi import FastAPI
import uvicorn
from app.routes import auth_routes, sport_routes

app = FastAPI(title="Babyfoot API", description="API pour gérer les joueurs de babyfoot", version="1.0.0")

app.include_router(auth_routes.router)
app.include_router(sport_routes.router)

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API de babyfoot!"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)