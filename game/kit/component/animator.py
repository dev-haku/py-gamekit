from game.kit.component.base_component import BaseComponent

class Animator(BaseComponent):
    def __init__(self, animations:dict, fps: float = 10.0, autoplay: bool = False):
        super().__init__()
        self.animations = animations
        self.current_animation_index = 0
        self.current_frame_index = 0
        self.frame_duration = 1.0 /fps
        self._elapsed = 0
        self.is_playing = autoplay
        self._parent_sprite = None

    def change_animation(self, animation_index):
        self.current_animation_index = animation_index

    def play(self):
        self.is_playing = True     

    def stop(self):
        self.is_playing = False
    
    def update(self, context):
        if not self.is_playing:
            return

        self._tick(dt= context.delta_time)
        self._apply_frame()

    def _tick(self, dt: float) -> None:
        animation_frames = self.animations[self.current_animation_index]
        
        self._elapsed += dt
        if self._elapsed >= self.frame_duration:
            self.current_frame_index = (self.current_frame_index + 1) % len(animation_frames)
            self._elapsed = 0

    def _apply_frame(self) -> None:
        if self._parent_sprite is None:
            self._parent_sprite = self.parent_gameobject.get_component("Sprite")
            if self._parent_sprite is None:
                return
            
        frame = self.animations[self.current_animation_index][self.current_frame_index].copy()
        self._parent_sprite.surface = frame.copy()