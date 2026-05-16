from game.kit.gameobject.base_gameobject import BaseGameobject
from game.kit.component.transform import Transform

class BaseWorldobject(BaseGameobject):
    def __init__(self):
        super().__init__()
        self.add_component(Transform())