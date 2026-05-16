from game.kit.gameobject.worldobject.base_worldobject import BaseWorldobject

class Camera(BaseWorldobject):
    
    def __init__(self):
        super().__init__()
        self.tags.append("camera")