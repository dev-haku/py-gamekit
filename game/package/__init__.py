from .core.scene import Scene
from .core.gameobject import Gameobject
from .core.component import Component

from .core.transform import Transform, RectTransform
from .core.sprite_renderer import SpriteRenderer, SimpleSpriteRenderer
from .core.collider import Collider

from .gameobjects.square import Square
from .gameobjects.ui import Image, Text

from .components.animator import Animator
from .components.timer import Timer

print("Loaded game package")