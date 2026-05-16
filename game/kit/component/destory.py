from game.kit.component.base_component import BaseComponent

class Destroy(BaseComponent):
    def __init__(self):
        super().__init__()
        self.do_destroy = False
    
    def update(self, engine):
        if self.do_destroy:
            if engine is not None:
                current_scene = engine.get("current_scene")
                current_scene.game_objects.remove(self.parent_gameobject)

        return super().update(engine)
        