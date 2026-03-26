from fastapi import APIRouter, HTTPException, Depends
from app.schemas.sport import Player, PlayerCreate
from app.security import get_current_user
from app.schemas.sport import Team, TeamCreate

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

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# partie équipe
fake_teams_db = []

@router.post("/teams", response_model=Team)
def create_team(
    team_data: TeamCreate, 
    current_user: str = Depends(get_current_user)
):
    # 1. Vérifier si les joueurs existent
    player_ids = [p["id"] for p in fake_players_db]
    if team_data.player1_id not in player_ids or team_data.player2_id not in player_ids:
        raise HTTPException(status_code=404, detail="L'un des joueurs n'existe pas")

    new_team = {
        "id": len(fake_teams_db) + 1,
        "name": team_data.name,
        "player1_id": team_data.player1_id,
        "player2_id": team_data.player2_id
    }
    
    fake_teams_db.append(new_team)
    return new_team

@router.get("/teams", response_model=list[Team])
def get_teams():
    return fake_teams_db