from __future__ import annotations

from dataclasses import dataclass
import asyncio
import time
import tomllib
from enum import IntEnum
from typing import TYPE_CHECKING, Final

import pygame

from ... import paths, definition
from .exceptions import PyGamekitError

if TYPE_CHECKING:
    from .scene import Scene

@dataclass(frozen=True)
class DebugConfig:
    show_colliders: bool
    print_key_events: bool
    show_performance: bool

class Engine:  

    def __init__(self):

        with open(paths.ROOT / "config.toml", "rb") as f:
            config: dict = tomllib.load(f)

        self.running: bool = False
        self.delta_time: float = 1.0 / config["max_tps"]
        self.global_values = definition.global_values
        self.debug_config = DebugConfig(**config["debug"])

        self.keyboard = Keyboard()
        self.mouse = Mouse()
        self.scheduler = Scheduler()

        pygame.init()

        flags = 0
        if config["window"]["resizable"]:
            flags |= pygame.RESIZABLE

        if config["window"]["fullscreen"]:
            flags |= pygame.FULLSCREEN

        self.window = pygame.display.set_mode(
            (config["window"]["width"], config["window"]["height"]), 
            flags
        )

        self.screen_size = (config["screen"]["width"], config["screen"]["height"])

        pygame.display.set_caption(config["title"])
        pygame.display.set_icon(pygame.image.load(paths.ROOT / config["icon_image_path"]))

        self.scenes: list[Scene] = definition.scenes
        self._init_scene_index: int = definition.initial_scene_index
        self.current_scene: Scene

        self.max_tps: int = config["max_tps"]
        self.max_fps: int = config["max_fps"]

    async def start(self):
        self.set_scene(self._init_scene_index)
        self.running = True
        await self._loop()

    def current_time(self):
        return time.time()
    
    def set_scene(self, index: int) -> None:
        if not 0 <= index < len(self.scenes):
            raise PyGamekitError(
                f"Engine: scene index が範囲外です。index={index}, "
                f"scenes_count={len(self.scenes)}"
            )

        context = {"engine" : self}
        self.current_scene = self.scenes[index](context)

    def shutdown(self):
        self.running = False

    async def _loop(self) -> None:
        clock = pygame.time.Clock()
        accumulator = 0.0

        tps_timer = 0.0
        tps_count = 0

        fps_timer = 0.0
        fps_count = 0

        tps = 0

        while self.running:
            dt = clock.tick(self.max_fps) / 1000
            await asyncio.sleep(0)

            accumulator += min(dt, self.delta_time * 5)
            fps_timer += dt
            tps_timer += dt

            while accumulator >= self.delta_time:
                self._update()
                accumulator -= self.delta_time
                tps_count += 1

            self._draw()
            fps_count += 1

            if tps_timer >= 2.0:
                tps = tps_count / tps_timer
                tps_timer = 0.0
                tps_count = 0

            if fps_timer >= 2.0:
                fps = fps_count / fps_timer

                if self.debug_config.show_performance:
                    print(f"{tps:.1f} ticks, {fps:.1f} fps")

                fps_timer = 0.0
                fps_count = 0

    def _update(self):
        events = pygame.event.get()
        self._process_events(events)
        self.keyboard.update(events, self)
        self.mouse.update(events)
        self.scheduler.update(self.delta_time)
        self.current_scene.update()

    def _process_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.shutdown()
                           
    def _draw(self):

        self.window.blit(
            pygame.transform.scale(
                self._render(), 
                self.window.get_size()
            ),
            (0,0)
        )

        pygame.display.flip()

    def _render(self) -> pygame.Surface:

        scene = self.current_scene

        if scene is None:
            raise PyGamekitError("Engine: current_scene が None です。")

        camera = scene.get_gameobject("Camera")
        if not self._get_state(camera):
            raise PyGamekitError("Engine: current_sceneに Cameraがない。")

        camera_transform = camera.get_component("Transform")
        if not self._get_state(camera_transform):
            raise PyGamekitError("Engine: current_sceneの CameraにTransformコンポーネントが付けられてない。")

        sw, sh = self.screen_size
        
        world_screen: pygame.Surface = pygame.Surface((
            max(1, int(sw // camera.zoom)),
            max(1, int(sh // camera.zoom))
        ))

        canvas_screen: pygame.Surface = pygame.Surface(
            (sw,sh), 
            pygame.SRCALPHA
        )

        world_screen.fill((0, 0, 0))
        canvas_screen.fill((0, 0, 0, 0))
        
        camera_position = camera_transform.position.xy
        camera_anchor = camera.anchor

        render_data_list = [
            render_data
            for go in scene.gameobjects
            for render_data in go.get_active_render_datas()
        ]

        render_data_list.sort(key=lambda x: x.layer)  

        for render_data in render_data_list:

            draw_surf = render_data.surface
            gameobject_position = render_data.position

            draw_targets = {
                "RectTransform" : {
                    "to": canvas_screen,
                    "pos" : (
                        gameobject_position.x - (draw_surf.get_size()[0] // 2) // 2,
                        gameobject_position.y - (draw_surf.get_size()[1] // 2) // 2
                    ),
                },

                "Transform" : {
                    "to" : world_screen,
                    "pos" : (
                        (gameobject_position[0] - camera_position[0]) + camera_anchor[0],
                        (gameobject_position[1] - camera_position[1]) + camera_anchor[1]
                    ),
                },
            }

            info: dict = draw_targets[render_data.transform_type]
            to_screen: pygame.Surface = info["to"]
            draw_pos: tuple[float,float] = info["pos"]

            camera_rect = pygame.Rect(
                0,
                0,
                to_screen.get_width(),
                to_screen.get_height(),
            )
                
            other_gameobject_rect = pygame.Rect(
                draw_pos[0],
                draw_pos[1],
                draw_surf.get_width(),
                draw_surf.get_height(),
            )
                
            if not camera_rect.colliderect(other_gameobject_rect):
                continue

            to_screen.blit(
                source= draw_surf,
                dest= draw_pos,  
            ) 

        screen = pygame.transform.scale(world_screen, (sw, sh))
        screen.blit(canvas_screen, (0,0))

        return screen

    def _get_state(self, obj):

        if obj is None:
            return False
    
        if not obj.active:
            return False
    
        return True

    
class Keyboard:
    def __init__(self):
        self._keys = {}

    def pressed(self, key):
        return self._keys.get(key, False)


    def update(self, events, engine):
        for event in events:
    
            if event.type == pygame.KEYDOWN:
                self._keys[pygame.key.name(event.key)] = True

                if engine.debug_config.print_key_events:
                    print(pygame.key.name(event.key))

            elif event.type == pygame.KEYUP:
                self._keys[pygame.key.name(event.key)] = False

class MouseButton(IntEnum):
    LEFT = 1
    MIDDLE = 2
    RIGHT = 3
    X1 = 4
    X2 = 5

class Mouse:
    def __init__(self):
        self._cursor_position = pygame.Vector2()
        self._buttons = {}

    @property
    def cursor_position(self):
        return self._cursor_position.copy()

    def pressed(self, button):
        return self._buttons.get(button, False)

    def left_pressed(self):
        return self.pressed(MouseButton.LEFT)

    def right_pressed(self):
        return self.pressed(MouseButton.RIGHT)

    def middle_pressed(self):
        return self.pressed(MouseButton.MIDDLE)

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                self._cursor_position = event.pos
                    
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._buttons[event.button] = True
                    
            elif event.type == pygame.MOUSEBUTTONUP:
                self._buttons[event.button] = False

 
class Scheduler:
    def __init__(self):
        self.events = []

    def schedule_event(self, delay, callback, *args, **kwargs):
        self.events.append({
            "time": delay,
            "callback": callback,
            "args" : args,
            "kwargs" : kwargs
        })

    def update(self, delta_time):
        for event in self.events[:]:
            event["time"] -= delta_time

            if event["time"] <= 0:
                self.events.remove(event)
                event["callback"](
                    *event["args"],
                    **event["kwargs"]
                )