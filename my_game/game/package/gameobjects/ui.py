import pygame

from ..core.gameobject import Gameobject
from ..core.sprite_renderer import SpriteRenderer
from ..core.transform import RectTransform


class Image(Gameobject):
    def __init__(
            self, 
            engine, scene, parent, name,
            position: tuple[float, float], 
            scale: tuple[float, float], 
            layer: int, 
            surface: pygame.Surface
        ) -> None:
        super().__init__(engine, scene, parent, name)

        transform = self.add_component(RectTransform)
        transform.position = position
        transform.scale = scale
        transform.layer = layer

        sprite_renderer = self.add_component(SpriteRenderer, surface)
        sprite_renderer.set_surface(surface)

    def set_image(self, surface: pygame.Surface) -> None:
        self.sprite_renderer.set_surface(surface)


class Text(Gameobject):
    def __init__(
        self, 
        engine, scene, parent, name,
        position: tuple[float,float],
        scale: tuple[float,float],
        layer: int,
        text: str,
        size: int,
        color: tuple[int,int,int],
        init_active: bool
    ) -> None:
        super().__init__(engine, scene, parent, name)

        self.active = init_active

        transform = self.add_component(RectTransform)
        transform.position = position
        transform.scale = scale
        transform.layer = layer
    
        self.font = pygame.font.SysFont(None, size)
        self.text: str = str(text) or "None"
        self.color: tuple[int,int,int] = color or (255,255,255)

        self.add_component(SpriteRenderer, surface= self._get_text_surface())

        self.flag = True

        self.dt = self.engine.delta_time
    
    def update(self) -> None:
        if self.flag == True:
            self.get_component("SpriteRenderer").surface = self._get_text_surface()
            self.flag = False

        return super().update()

    def set_text(self, text: str) -> None:
        self.text = str(text)
        self.flag = True

    def set_color(self, color: tuple[int,int,int]) -> None:
        self.color = tuple(color)
        self.flag = True

    def _get_text_surface(self) -> pygame.Surface:
        return self.font.render(self.text, True, self.color)
        