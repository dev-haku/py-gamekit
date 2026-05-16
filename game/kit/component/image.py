import pygame
from game.kit.component.base_component import BaseComponent

class Image(BaseComponent):
    def __init__(self):
        super().__init__()
        self.original_surface = None
        self.surface = None

        self.surface_dirty = False

        self.cached_parent_data = {"size": [0,0],"scale": [1,1]}

    def start(self, engine):
        self.parent_recttransform = self.parent_gameobject.get_component("RectTransform")

    def update(self, engine):

        if self.parent_recttransform is None:
            return
        
        if self.original_surface is not None:
            if(
               self.surface_dirty or
               self.parent_recttransform.size.xy != self.cached_parent_data["size"] or
               self.parent_recttransform.scale.xy != self.cached_parent_data["scale"]
               ):
                
                self.scale_surface()
                self.cache()

        return super().update(engine)

    def scale_surface(self):
        size = (
            self.parent_recttransform.size.x * self.parent_recttransform.scale.x, 
            self.parent_recttransform.size.y * self.parent_recttransform.scale.y
            )
        self.surface = pygame.transform.scale(self.original_surface, size)

    def cache(self):
        self.cached_parent_data["size"] = self.parent_recttransform.size.xy
        self.cached_parent_data["scale"] = self.parent_recttransform.scale.xy
                
    def set_surface(self, surface: pygame.Surface) -> None:
        if not isinstance(surface, pygame.Surface):
            raise TypeError("surface must be pygame.Surface")
        
        self.original_surface = surface
        self.surface_dirty = True
    
    def get_surface(self) -> pygame.Surface | None:
        return self.surface