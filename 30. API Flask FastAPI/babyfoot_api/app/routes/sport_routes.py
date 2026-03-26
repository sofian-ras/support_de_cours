from fastapi import APIRouter, HTTPException, Depends
from app.schemas.sport import Player, PlayerCreate
from app.security import get_current_user

router = APIRouter(prefix="/sport", tags=["Babyfoot"])

fake_players_db = []

@router.post("/players", response_model=Player)
def create_player(
    player_data: PlayerCreate, 
    current_user: str = Depends(get_current_user)
):

    if any(p["nickname"] == player_data.nickname for p in fake_players_db):
        raise HTTPException(status_code=400, detail="ce joueur existe déjà")
    
    new_player = {
        "id": len(fake_players_db) + 1,
        "nickname": player_data.nickname
    }
    fake_players_db.append(new_player)
    return new_player