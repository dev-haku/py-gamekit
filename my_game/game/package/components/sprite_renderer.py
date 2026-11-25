import pygame

from ..util.get_scaled_surface import get_scaled_surface
from ..core.component import Component
from ..core.render_data import RenderData
from .transform import RectTransform, Transform


class SpriteRenderer(Component):

    def __init__(
        self,
        context,
        surface: pygame.Surface | None = None
    ) -> None:
        super().__init__(context)

        self._original_surface: pygame.Surface = surface
        self._offset_position = pygame.Vector2()
        self._flag = True
        self.rotation_angle = 0

        self._parent_transform: Transform = self.parent.get_component("Transform")
        if self._parent_transform is None:
            self._parent_transform: RectTransform = self.parent.get_component("RectTransform")

        self.render_data.active = True
        self.render_data.transform_type = self._parent_transform.__class__.__name__

    @property
    def surface(self) -> pygame.Surface:
        return self._original_surface

    @surface.setter
    def surface(self, surface : pygame.Surface):
        self._original_surface = surface
        self._flag = True

    @property
    def scaled_size(self) -> tuple[float, float]:
        return (
            self._original_surface.get_width() * self._parent_transform.scale.x,
            self._original_surface.get_height() * self._parent_transform.scale.y
        )

    @property
    def offset_position(self) -> pygame.Vector2:
        return self._offset_position

    @offset_position.setter
    def offset_position(self, x:float, y:float):
        self._offset_position = pygame.Vector2(x, y)

    def update(self):

        if self._flag:
            
            # original_surface_size = self.original_surface.get_size()
            # parent_scale = self.transform.scale.xy
        

            # surface = pygame.Surface((original_surface_size[0]*2, original_surface_size[1]*2))
            # surface.fill((0,255,0))
  
            # sw, sh = surface.get_size()
            # surface.blit(
            #     self.original_surface, 
            #     (
            #         sw/2 - original_surface_size[0]/2,
            #         sh/2 - original_surface_size[1]/2)
            #     )

            # rotated_surface = pygame.transform.rotate(surface, self.rotation_angle) 

            # scaled_surface = pygame.transform.scale(
            #     rotated_surface, 
            #     (
            #         rotated_surface.get_width() * parent_scale[0],
            #         rotated_surface.get_height() * parent_scale[1]
            #     )
            # )

            # self.render_data.surface = scaled_surface


            scaled_surface = pygame.transform.scale(
                self._original_surface, 
                self.scaled_size
            )
        
            surface = pygame.Surface((scaled_surface.get_width()*2, scaled_surface.get_height()*2), pygame.SRCALPHA)
            surface.blit(
                scaled_surface, 
                (
                    surface.get_width()/2 - scaled_surface.get_width()/2,
                    surface.get_height()/2 - scaled_surface.get_height()/2)
                )

            rotated_surface = pygame.transform.rotate(surface, self.rotation_angle) 

            self.render_data.surface = rotated_surface

            self._flag = False

        self.render_data.position.xy = (
            self._parent_transform.position.x + self._offset_position.x - self.render_data.surface.get_width()/4, 
            self._parent_transform.position.y + self._offset_position.y - self.render_data.surface.get_height()/4
        )
        
        self.render_data.layer = self._parent_transform.layer

        return super().update()

    def set_rotation_angle(self, angle_value):
        self.rotation_angle = angle_value
        self._flag = True


class SimpleSpriteRenderer(Component):
    def __init__(self, context, surface: pygame.Surface):
        super().__init__(context)
        self._original_surface: pygame.Surface = surface
        self._offset_position = pygame.Vector2()

        self._parent_transform: Transform = self.parent.get_component("Transform")
        if self._parent_transform is None:
            self._parent_transform: RectTransform = self.parent.get_component("RectTransform")

        self.render_data.active = True
        self.render_data.transform_type = self._parent_transform.__class__.__name__
        self.render_data.surface = get_scaled_surface(self._original_surface, (self._parent_transform.scale.x, self._parent_transform.scale.y))

    @property
    def scaled_size(self):
        return (
            self._original_surface.get_width() * self._parent_transform.scale.x,
            self._original_surface.get_height() * self._parent_transform.scale.y
        )

    @property
    def offset_position(self) -> pygame.Vector2:
        return self._offset_position

    @offset_position.setter
    def offset_position(self, value: tuple[float,float]):
        self._offset_position = pygame.Vector2(value)
        
    def update(self):
        self.render_data.position.xy = (
            self._parent_transform.position.x + self._offset_position.x, 
            self._parent_transform.position.y + self._offset_position.y
        )

        self.render_data.layer = self._parent_transform.layer

        return super().update()