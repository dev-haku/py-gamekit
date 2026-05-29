import pygame

from game.kit.component.base_component import BaseComponent, Renderer


class AnimationData:

    def __init__(
            self,
            name: str,
            frames: list[pygame.Surface],
            fps: float,
            is_loop: bool
        ):
        self.name: str = name
        self.frames: list[pygame.Surface] = frames
        self.fps: float = fps
        self.is_loop: bool = is_loop

        self._scaled_cache: dict[tuple[float, float], list[pygame.Surface]] = {}

    def get_scaled_frames(self, scale: tuple[float, float]) -> list[pygame.Surface]:
        if scale not in self._scaled_cache:
            self._scaled_cache[scale] = self._build_scaled_frames(scale)
        return self._scaled_cache[scale]

    def _build_scaled_frames(self, scale: tuple[float, float]) -> list[pygame.Surface]:
        sx, sy = scale
        return [
            pygame.transform.scale(
                frame,
                (int(frame.get_width() * sx), int(frame.get_height() * sy))
            )
            for frame in self.frames
        ]


class AnimationPlayer():

    def __init__(self):
        self.animation: AnimationData | None = None
        self.is_playing: bool = False
        self.frame_index: int = 0
        self.elapsed: float = 0.0


    def update(self, dt: float) -> None:
        if self.is_playing:

            if self.animation is None:
                return

            frame_duration = 1.0 / self.animation.fps
            self.elapsed += dt

            if self.elapsed >= frame_duration:
                self.elapsed -= frame_duration
                next_index = self.frame_index + 1

                if next_index >= len(self.animation.frames):
                    if self.animation.is_loop:
                        self.frame_index = 0
                    else:
                        self.frame_index = len(self.animation.frames) - 1
                        self.is_playing = False
                else:
                    self.frame_index = next_index


    def play(self) -> None:
        self.is_playing = True

    def stop(self) -> None:
        self.is_playing = False

    def reset(self) -> None:
        self.frame_index = 0
        self.elapsed = 0.0


class Animator():

    def __init__(self):
        super().__init__()
        self.animations: list[AnimationData] = []
        self.animation_player: AnimationPlayer = AnimationPlayer()


    def start(self) -> None:
        if len(self.animations) >= 1:
            self.animation_player.animation = self.animations[0]

    def update(self, engine):
        self.animation_player.update(engine.delta_time)


    def add_animation(
        self,
        name: str,
        frames: list[pygame.Surface],
        fps: float,
        is_loop: bool
    ) -> None:
        self.animations.append(AnimationData(name, frames, fps, is_loop))

    def remove_animation(self, name: str) -> None:
        self.animations = [a for a in self.animations if a.name != name]


    def change_animation(self, name: str, autoplay: bool = False, force_restart: bool = False) -> None:

        animation = self.animation_player.animation
        if animation is not None:
            if animation.is_loop == True and animation.name == name:
                return
            
        animation = self._find_animation(name)
        if animation is None:
            return
        
        self.animation_player.animation = animation

        if autoplay:
            self.animation_player.play()
        else:
            self.animation_player.stop()

        if force_restart:
            self.animation_player.reset()

    def _find_animation(self, name: str) -> AnimationData | None:
        for animation in self.animations:
            if animation.name == name:
                return animation
        print(
            f"{self.parent_gameobject}, {self.__class__.__name__}: "
            f"アニメーション '{name}' が見つかりませんでした。"
        )
        return None

class AnimationRenderer(BaseComponent):

    def __init__(self) -> None:
        super().__init__()
        self.animator = Animator()
        self.renderer = Renderer()

    def start(self, engine):
        self.animator.start()
        self.transform = self.parent_gameobject.get_component("Transform")
        return super().start(engine)

    def update(self, engine) -> None:
        self.animator.update(engine)

        animation_player: AnimationPlayer  = self.animator.animation_player
        if animation_player.animation is None:
            return super().update(engine)
        
        frames = animation_player.animation.get_scaled_frames(self._get_current_parent_scale())

        self.renderer.surface = frames[animation_player.frame_index]
        self.renderer.position = self.transform.position
        self.renderer.layer = self.transform.layer

        return super().update(engine)
    
    def _get_current_parent_scale(self) -> tuple[float, float]:
        if self.transform is None:
            return (1.0, 1.0)
        scale = self.transform.scale

        return (scale.x, scale.y)