from game.package.base_object import BaseScene
from game.package.gameobject.worldobject.square import Square
from .player import Player
from .ui import Image
from .move_square import MoveSquare


class GameScene(BaseScene):

    def start(self, engine):
        player = Player((-100,0), (2,2),4)
        
        self.add_worldobject(player)
        for x in range(1):
            for y in range(10):
                square = MoveSquare((x*100,y*100),(1,1), 2, (255,255,255))
                self.add_worldobject(square)

        image = Image((0.15,0.9), (100,50), (1,1), 1)
        self.add_uiobject(image)
    
        return super().start(engine)