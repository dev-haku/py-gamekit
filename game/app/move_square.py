from game.package.gameobject.worldobject import Square
from game.package.base_object import BaseComponent

class MoveSquare(Square):
    def __init__(self, position, scale, layer, color = ...):
        super().__init__(position, scale, layer, color)

        self.add_component(Controller())

class Controller(BaseComponent):
    
    def start(self, engine):
        self.transform = self.parent_gameobject.get_component("Transform")
        return super().start(engine)
        
    def update(self, engine):
        dt = engine.delta_time
        self.transform.position.x += 10 *dt
        self.transform.position.y += 10 *dt
        self.transform.scale.x += 1 *dt
        self.transform.scale.y += 1 *dt
        return super().update(engine)