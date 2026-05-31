from game.package.base_object.gameobject import BaseGameobject
from game.package.component.transform import Transform

class BaseWorldobject(BaseGameobject):
    def __init__(self):
        super().__init__()
        self.add_component(Transform())