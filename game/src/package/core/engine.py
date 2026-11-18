from __future__ import annotations
import pygame
import asyncio
import json
import time
import pathlib

from src import config, definition


from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.package.core.scene import Scene


class Engine:  

    def __init__(self):

        self.running: bool = False
        self.delta_time: float = 0
        self.global_values: dict = definition.global_values
        self.input_status: InputStatus = InputStatus()
        self.scheduler:  Scheduler = Scheduler()
        self.debug_settings = definition.debug
    
        pygame.init()

        self.window = pygame.display.set_mode(
            config.WINDOW_SIZE, 
            pygame.RESIZABLE
        )

        pygame.display.set_caption(config.NAME)
        pygame.display.set_icon(pygame.image.load(config.ICON_IMAGE_PATH))

        self.scenes: list = definition.scenes

        self.init_scene_index = definition.initial_scene_index
        self.current_scene: Scene = None

        self.max_tps: int = config.MAX_TPS
        self.max_fps: int = config.MAX_FPS

    async def start(self):
        self.running = True
        await self._loop()

    def current_time(self):
        return time.time()

    def change_scene(self, index: int):
        self.current_scene = self.scenes[index](engine=self)

    def shutdown(self):
        self.running = False

    async def _loop(self):
        clock = pygame.time.Clock()
        accumulator = 0.0
        fixed_dt = 1.0 / self.max_tps

        tps_timer = 0
        tps_count = 0
        fps_timer = 0
        fps_count = 0
        tps = 0

        while self.running:
            dt = clock.tick(self.max_fps) / 1000
            await asyncio.sleep(0)  
            accumulator += min(dt, fixed_dt * 5)

            fps_timer += dt

            while accumulator >= fixed_dt:
                self.delta_time = fixed_dt
                self._update()

                accumulator -= fixed_dt
                
                tps_timer += fixed_dt
                tps_count += 1
            
            self._draw()
            fps_count += 1

            if tps_timer >= 1:     
                tps = tps_count
                tps_timer = 0
                tps_count = 0

            if fps_timer >= 1:
                print(f"{tps} ticks, {fps_count} fps")

                fps_timer = 0
                fps_count = 0

    def _update(self):
        if self.current_scene is None:
            self.current_scene = self.scenes[self.init_scene_index](engine= self)

        self._process_events()
        self.scheduler.update(self.delta_time)

        scene = self.current_scene
        if scene.active:
            scene.update()

    def _process_events(self):

        for event in pygame.event.get():
    
            if event.type == pygame.QUIT:
                self.shutdown()

            elif event.type == pygame.KEYDOWN:
                self.input_status.keys[pygame.key.name(event.key)] = True

                if self.debug_settings["print_key_events"]:
                    print(pygame.key.name(event.key))

            elif event.type == pygame.KEYUP:
                self.input_status.keys[pygame.key.name(event.key)] = False

            elif event.type == pygame.MOUSEMOTION:
                self.input_status.mouse_position = event.pos

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.input_status.mouse_buttons = [False] * 5
                self.input_status.mouse_buttons[event.button - 1] = True

            elif event.type == pygame.MOUSEBUTTONUP:
                self.input_status.mouse_buttons = [False] * 5
                                 
    def _draw(self):
        if self.current_scene is None:
            return

        if self.current_scene.active:

            screen = self.current_scene.render()

            scaled_screen = pygame.transform.scale(
                screen, 
                self.window.get_size()
            )

            self.window.blit(
                scaled_screen, 
                (0,0)
            )

        pygame.display.flip()


class InputStatus:
    def __init__(self):
        self.keys = {}
        self.mouse_position = (0,0)
        self.mouse_buttons = [False] * 5

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
                event["callback"](
                    *event["args"],
                    **event["kwargs"]
                )
                self.events.remove(event)