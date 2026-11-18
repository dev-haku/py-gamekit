from .core import Scene
from .core import Gameobject
from .core import Component

from .core.transform import Transform
from .core.transform import RectTransform
from .core.sprite_renderer import SpriteRenderer
from .core.sprite_renderer import SimpleSpriteRenderer


from .gameobjects.square import Square
from .gameobjects.ui import Image, Text

from .components.animator import Animator
from .core.collider import Collider
from .components.timer import Timer

print("Loaded game package")