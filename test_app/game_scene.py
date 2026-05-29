from game.kit.scene.base_scene import BaseScene
from .player import Player
from game.kit.gameobject.worldobject.square import Square
from .ui import Image


class GameScene(BaseScene):
    def start(self, engine):
        player = Player((-100,0), (2,2),4)
        square1 = Square((50,80),(10,40), 2)
        square2 = Square((50,0),(40,10), 2)
        
        self.add_worldobject(player)
        self.add_worldobject(square1)
        self.add_worldobject(square2)

        image = Image((0.15,0.9), (100,50), (1,1), 1)
        self.add_uiobject(image)
    
        return super().start(engine)