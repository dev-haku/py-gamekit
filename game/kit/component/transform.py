from pygame import Vector2
from game.kit.component.base_component import BaseComponent

class Transform(BaseComponent):
    def __init__(self):
        super().__init__()
        self._position: Vector2 = Vector2(0,0)
        self._size: Vector2 = Vector2(100,100)
        self._scale: Vector2 = Vector2(1,1)
        self._layer: int = 0

    @property
    def position(self) -> Vector2 | None:
        return self._position
    
    @position.setter
    def position(self, position: tuple):
        self._position = Vector2(position[0], position[1])

    @property
    def size(self) -> Vector2 | None:
        return self._size
    
    @size.setter
    def size(self, size: tuple):
        self._size = Vector2(size[0], size[1])

    @property
    def scale(self) -> Vector2 | None:
        return self._scale
    
    @scale.setter
    def scale(self, scale: tuple):
        self._scale = Vector2(scale[0], scale[1])

    @property
    def scaled_size(self) -> Vector2 | None:
        return Vector2(self._size.x * self._scale.x, self._size.y * self._scale.y)

    @property
    def layer(self) -> int | None:
        return self._layer
    
    @layer.setter
    def layer(self, layer: int):
        self._layer = layer
    
class RectTransform(Transform):
    def __init__(self):
        super().__init__()

    @Transform.position.setter
    def position(self, position: tuple):
        self._position = Vector2(
            max(0.0, min(1.0, position[0])),
            max(0.0, min(1.0, position[1]))
        )