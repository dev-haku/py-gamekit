from __future__ import annotations

from typing import TYPE_CHECKING

from .render_data import RenderData

if TYPE_CHECKING:
    from .engine import Engine
    from .gameobject import Gameobject
    from .scene import Scene


class Component:
    
    def __init__(self, context) -> None:
        
        self.engine: Engine = context["engine"]
        self.scene: Scene = context["scene"]

        self.active: bool = True
        self.tags: list[str] = []

        self._parent: Gameobject = context["parent"]

        self.render_data = RenderData()

    @property
    def parent(self):
        return self._parent

    def update(self) -> None:
        pass

        