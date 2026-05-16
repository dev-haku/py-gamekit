import pygame
from game.kit.component.base_component import BaseComponent

class Sprite(BaseComponent):
    _DEFAULT_TRANSFORM_CACHE = {"size": [0, 0], "scale": [1, 1]}

    def __init__(self):
        super().__init__()
        self.original_surface: pygame.Surface | None = None
        self._surface: pygame.Surface | None = None
        self.surface_dirty = False
        self._cached_transform = dict(self._DEFAULT_TRANSFORM_CACHE)

    def start(self, context):
        self.parent_transform = self.parent_gameobject.get_component("Transform")

    def update(self, context):
        if self.parent_transform is None:
            return

        if self.original_surface is not None and self._needs_rescale:
            self._scale_surface()
            self._cache()

        return super().update(context)

    @property
    def _needs_rescale(self) -> bool:
        t = self.parent_transform
        c = self._cached_transform
        return (
            self.surface_dirty
            or t.size.xy != c["size"]
            or t.scale.xy != c["scale"]
        )

    def _scale_surface(self):
        t = self.parent_transform
        size = (t.size.x * t.scale.x, t.size.y * t.scale.y)
        self._surface = pygame.transform.scale(self.original_surface, size)

    def _cache(self):
        t = self.parent_transform
        self._cached_transform["size"] = t.size.xy
        self._cached_transform["scale"] = t.scale.xy
        self.surface_dirty = False  # ← バグ修正: リセット忘れ

    @property
    def surface(self) -> pygame.Surface | None:
        return self._surface

    @surface.setter
    def surface(self, value: pygame.Surface) -> None:
        if not isinstance(value, pygame.Surface):
            raise TypeError(f"surface must be pygame.Surface, got {type(value).__name__}")
        self.original_surface = value
        self.surface_dirty = True
