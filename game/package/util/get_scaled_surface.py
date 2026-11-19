import functools
import pygame

@functools.cache
def get_scaled_surface(surface: pygame.Surface, scale: tuple[float,float]):
    return pygame.transform.scale(
        surface,
        (
            surface.get_width() * scale[0],
            surface.get_height() * scale[1]
        )
    )