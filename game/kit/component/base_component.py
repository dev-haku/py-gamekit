import pygame

from game.kit.util.make_empty_surface import make_empty_surface


class Renderer:
    def __init__(self):
        self.surface: pygame.Surface = make_empty_surface()
        self._position: pygame.Vector2 = pygame.Vector2(0,0)
        self.layer: int = 0

    @property
    def position(self):
        return self._position.copy()

    @position.setter
    def position(self, value: tuple[float,float]):
        self._position = pygame.Vector2(value[0], value[1])


class BaseComponent:
    def __init__(self):
        self.active: bool = True
        self._tags: list[str] = []
        self.is_started: bool = False
        self.parent_gameobject = None

    def start(self, engine):
        pass

    def update(self, engine):
        pass

    @property
    def tags(self) -> list[str]:
        return self._tags

    def add_tag(self, tag_name: str):
        self._tags.append(tag_name)