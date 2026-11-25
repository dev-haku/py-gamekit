from .components.animator import Animator
from .components.timer import Timer

from .core.collider import Collider
from .core.component import Component
from .core.gameobject import Gameobject
from .core.scene import Scene

from .gameobjects.square import Square
from .gameobjects.ui import Image, Text

from .components.sprite_renderer import SimpleSpriteRenderer, SpriteRenderer
from .components.transform import RectTransform, Transform
from .components.animator import Animator
from .components.timer import Timer


__all__ = [
    "Animator",
    "Timer",
    "Collider",
    "Component",
    "Gameobject",
    "Scene",
    "SimpleSpriteRenderer",
    "SpriteRenderer",
    "RectTransform",
    "Transform",
    "Square",
    "Image",
    "Text",
]


print("Loaded game package")
