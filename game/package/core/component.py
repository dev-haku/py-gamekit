from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .engine import Engine
    from .scene import Scene
    from .gameobject import Gameobject


class Component:
    
    def __init__(self, engine: Engine, scene: Scene, parent: Gameobject, kwargs: dict):

        self.engine = engine
        self.scene = scene
        self.parent = parent

        self.active: bool = True
        self.tags: list[str] = []

    def update(self):
        pass

    def add_tag(self, tag_name: str):
        self._tags.append(tag_name)

        