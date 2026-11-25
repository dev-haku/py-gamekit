from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .engine import Engine
    from .gameobject import Gameobject
    from .scene import Scene


class Component:
    
    def __init__(
        self, 
        engine: Engine, 
        scene: Scene, 
        parent: Gameobject
    ) -> None:
        self.engine = engine
        self.scene = scene

        self.active: bool = True
        self.tags: list[str] = []

        self._parent = parent

    @property
    def parent(self):
        return self._parent

    def update(self) -> None:
        pass

        