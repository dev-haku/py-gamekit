import pygame

from .component import Component


class Transform(Component):

    def __init__(self, engine, scene, parent):
        super().__init__(engine, scene, parent)

        self._position: pygame.Vector2 = pygame.Vector2(0,0)
        self._scale: pygame.Vector2 = pygame.Vector2(1,1)
        self.layer: int = 0

    @property
    def position(self) -> pygame.Vector2:
        return self._position
    
    @position.setter
    def position(self, value: tuple) -> None:
        self._position = pygame.Vector2(value[0], value[1])

    @property
    def scale(self) -> pygame.Vector2:
        return self._scale
    
    @scale.setter
    def scale(self, value: tuple) -> None:
        self._scale = pygame.Vector2(
            max(0, value[0]),
            max(0, value[1])
        )

    
class RectTransform(Component):

    def __init__(self, engine, scene, parent):
        super().__init__(engine, scene, parent)

        self._position: pygame.Vector2 = pygame.Vector2(0,0)
        self._scale: pygame.Vector2 = pygame.Vector2(1,1)
        self.layer: int = 0
        
        self._pos_ratio = (0,0)

    @property
    def position(self) -> pygame.Vector2:
        return self._position

    @position.setter
    def position(self, value: tuple) -> None:
        self._pos_ratio = (
            max(0.0, min(1.0, value[0])), 
            max(0.0, min(1.0, value[1]))
        )  

    @property
    def scale(self) -> pygame.Vector2:
        return self._scale
        
    @scale.setter
    def scale(self, value: tuple) -> None:
        self._scale = pygame.Vector2(
            max(0, value[0]),
            max(0, value[1])
        )
        
    def update(self):
        screen_size = self.engine.screen_size

        self._position = pygame.Vector2(
            screen_size[0] * self._pos_ratio[0],
            screen_size[1] * self._pos_ratio[1]
        )

        return super().update()