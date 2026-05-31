import pygame

from game.package.base_object.component import BaseComponent


class Sprite(BaseComponent):
    def __init__(self):
        super().__init__()
        self._original_surface: pygame.Surface | None = None
        self._parent_scale_cache: tuple[float, float] = (0.0, 0.0)

    def start(self, engine):
        a = self.parent_gameobject.get_component("Transform")
        b = self.parent_gameobject.get_component("RectTransform")
        if a is not None:
            self._parent_transform = a
        else:
            self._parent_transform = b

        self.renderer = self.parent_gameobject.get_component("Renderer")
        self.renderer.register_render_as(id(self))
        

        return super().start(engine)

    def update(self, engine):
        if self._original_surface is None:
            return super().update(engine)
        
        current_scale: tuple =  self._parent_transform.scale.xy
        if current_scale != self._parent_scale_cache:
            self._scale_surface(current_scale)

        return super().update(engine)
    
    def set_surface(self, surface: pygame.Surface) -> None:
        self._original_surface = surface
        self._parent_scale_cache = (0.0, 0.0)
    
    def _scale_surface(self, scale: tuple[float, float]) -> None:
        scale_x, scale_y = scale
        w, h = self._original_surface.get_size()
        
        obj = self.renderer.render_objects[id(self)]
        obj.surface = pygame.transform.scale(self._original_surface, (w * scale_x, h * scale_y))
        obj.position = tuple(self._parent_transform.position.xy)
        obj.layer = self._parent_transform.layer

        self._parent_scale_cache = scale