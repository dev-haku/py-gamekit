from __future__ import annotations
from typing import TYPE_CHECKING
import sys
import time

from .component import Component

if TYPE_CHECKING:
    from .engine import Engine
    from .scene import Scene


class Gameobject:
    
    def __init__(self, engine: Engine, scene: Scene, kwargs: dict) -> None:

        self.engine: Engine = engine
        self.scene: Scene = scene

        self.active: bool = True 
        self.name: str = None
        self.tags: list[str] = []

        self.parent = None
        self.children:list[Gameobject] = []
        self.components: dict[str, Component] = {}
        
        self.created_timestamp: float = time.time()

    def update(self):
        pass

    def add_child(self, gameobject_class: type[Gameobject],  name: str = None, **kwargs):

        gameobject = gameobject_class(self.engine, self.scene, kwargs)

        if name is None:
            find_target_name = gameobject.__class__.__name__
            count = 1
            for obj in self.scene.gameobjects:
                if obj.__class__.__name__ == find_target_name:
                    count += 1
            
            if count > 1:
                gameobject.name = f"{gameobject.__class__.__name__}{count}"
            else:
                gameobject.name = gameobject.__class__.__name__
        else:
            gameobject.name = name

        gameobject.parent = self
        self.children.append(gameobject)

        self.scene.gameobjects.append(gameobject)

        return gameobject

    def get_child(self, target_name: str):
        for name, _id in self.children.items():
            if name == target_name:
                return self.engine.current_scene.get_worldobject(_id)
        return None
    
    def add_component(self, component_class: type[Component], **kwargs: dict) -> Component:
        comp = component_class(self.engine, self.scene, self, kwargs)
        if self.engine is None:
            print(f"{self.__class__.__name__}の self.engineがNoneで{comp.__class__.__name__}に代入できなかった",file=sys.stderr)
        self.components[comp.__class__.__name__] = comp

        return comp

    def remove_component(self, target_name):
        for name in self.components.keys():
            if name == target_name:
                del self.components[name]
                return

    def get_component(self, target_name: str) -> Component | None:
        for name, comp in self.components.items():
            if name == target_name:
                return comp
        return None
    
    def destroy(self):
        for gameobject in self.scene.gameobjects:
            if self == gameobject:
                self.scene.gameobjects.remove(gameobject)
                return