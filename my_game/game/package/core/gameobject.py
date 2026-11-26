from __future__ import annotations
from typing import TYPE_CHECKING
import time

from .component import Component
from .exceptions import PyGamekitError

if TYPE_CHECKING:
    from .render_data import RenderData
    from .engine import Engine
    from .scene import Scene


class Gameobject:
    
    def __init__(
        self, 
        context
    ) -> None:
        self.engine: Engine = context["engine"]
        self.scene: Scene = context["scene"]

        self.active: bool = True 
        self.name = context["name"]
        self.tags: list[str] = []

        self._parent = context["parent"]
        self._children:list[Gameobject] = []
        self._components: dict[str, Component] = {}
        
        self.created_timestamp: float = time.time()

    @property
    def parent(self) -> Gameobject | None:
        return self._parent

    def add_child(
        self,
        gameobject_class: type[Gameobject],
        name: str | None = None,
        **kwargs
    ) -> Gameobject:
        
        class_name = gameobject_class.__name__

        if name is None or name == class_name:

            existing_names = {
               obj.name for obj in self.scene.gameobjects
            }

            name = class_name
            count = 1

            while name in existing_names:
                name = f"{class_name}{count}"
                count += 1

        context = {
            "engine" : self.engine, 
            "scene" : self.scene, 
            "parent" : self, 
            "name" : name
        }

        go = gameobject_class(context, **kwargs)

        self._children.append(go)
        self.scene.gameobjects.append(go)

        return go

    def get_child(self, target_name: str) -> Gameobject | None:
        for child in self._children:
            if child.name == target_name:
                return child
        return None

    def remove_child(self, gameobject: Gameobject) -> Gameobject:
        if gameobject not in self._children:
           raise PyGamekitError(f"{self.__class__.__name__} の self.engine が None")

        self._children.remove(gameobject)
        gameobject._parent = None

    def add_component(self, component_class: type[Component], **kwargs) -> Component:

        if self.engine is None:
            raise PyGamekitError(f"{self.__class__.__name__} の self.engine が None")

        context = {
            "engine" : self.engine, 
            "scene" : self.scene, 
            "parent" : self, 
        }

        comp = component_class(context, **kwargs)
        self._components[comp.__class__.__name__] = comp

        return comp

    def remove_component(self, target_name: str) -> None:
        self._components.pop(target_name, None)

    def get_component(self, target_name: str) -> Component | None:
        return self._components.get(target_name)

    def get_active_render_datas(self) -> list[RenderData]:
        return [
            comp.render_data
            for comp in self._components.values()
            if hasattr(comp, "render_data")
            and comp.render_data.active
        ]
    
    def destroy(self) -> None:
        for child in self._children.copy():
            child.destroy()

        if self.parent is not None:
            self.parent.remove_child(self)

        self.scene.remove_gameobject(self)

    def update(self) -> None:
        for comp in self._components.values():       
            comp.update()