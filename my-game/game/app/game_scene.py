from game.package import (
    Scene,
    Square,
    Image
)

from .player import Player


class GameScene(Scene):

    def start(self):

        w, h = self.engine.screen.get_size()
        self.camera.anchor = (w//2, h//2)

        player = Player((-100,0), (4,4),4)
        self.add_worldobject(player)

        square = Square((0,0), (20,20), 1, (0,0,255), (0,255,0))
        self.add_worldobject(square)

        image = Image((0.15,0.9), (100,50), (1,1), 1)
        self.add_uiobject(image)
    
        return super().start()