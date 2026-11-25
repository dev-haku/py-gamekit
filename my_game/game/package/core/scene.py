from __future__ import annotations

from typing import TYPE_CHECKING

from .camera import Camera
from .collision_system import CollisionSystem

if TYPE_CHECKING:
    from .engine import Engine
    from .gameobject import Gameobject


class Scene:
    
    def __init__(self, engine: Engine) -> None:
        self.engine: Engine = engine

        self.gameobjects: list[Gameobject] = [] 
        
        self.add_gameobject(CollisionSystem)
        self.add_gameobject(Camera)

    def add_gameobject(self, gameobject_class: type[Gameobject], name: str = None, **kwargs) -> Gameobject:

        class_name = gameobject_class.__name__

        if name is None or name == class_name:

            existing_names = {
               obj.name for obj in self.gameobjects
            }

            name = class_name
            count = 1

            while name in existing_names:
                name = f"{class_name}{count}"
                count += 1

        go = gameobject_class(
            engine= self.engine, 
            scene= self, 
            parent= None, 
            name= name, 
            **kwargs
        )

        self.gameobjects.append(go)

        return go

    def get_gameobject(self, target_gameobject_name: str) -> Gameobject | None:
        for go in self.gameobjects:
            if go.name == target_gameobject_name:
                return go
            
        return None

    def remove_gameobject(self, target_gameobject: Gameobject) -> Gameobject:
        if target_gameobject in self.gameobjects:
            self.gameobjects.remove(target_gameobject)

    def update(self) -> None:
        for go in self.gameobjects:
            go.update()