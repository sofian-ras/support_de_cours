from pydantic import BaseModel, Field, model_validator
class PlayerCreate(BaseModel):
    nickname: str = Field(..., min_length=3, max_length=20)

class Player(PlayerCreate):
    id: int


# on verifie qu'on ne met pas deux fois le meme player
class TeamCreate(BaseModel):
    name: str = Field(..., min_length=3)
    player_1_id: int
    player_2_id: int

    @model_validator(mode="after")
    def check_different_players(self):
        if self.player_1_id == self.player_2_id:
            raise ValueError("Les deux joueurs doivent être différents")
        return self