from core.object import GameObject
from script.movement import Movement

class Player(GameObject):
    player_id: str

    def __init__(self, player_id: str):
        super().__init__()
        self.player_id = player_id
        self.name = f'#{player_id}'
        self.attach(Movement('Movement'))
