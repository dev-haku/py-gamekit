from dataclasses import dataclass
import pygame
import time

from game import config


class Engine:  

    def __init__(self):
        pygame.init()

        self.window = pygame.display.set_mode(
            config.game["window_size"], 
            pygame.RESIZABLE
        )

        pygame.display.set_caption(config.game["name"])
        pygame.display.set_icon(pygame.image.load(config.game["icon_image_path"]))
        
        self.running = False

        self.screen = pygame.Surface(config.game["screen_size"])
        init_scene_class = config.game["initial_scene_class"]
        self.current_scene = init_scene_class()

        self.max_tps = config.game["max_tps"]
        self.max_fps = config.game["max_fps"]

        self.delta_time = 0

        self.input_status = InputStatus()

    def start(self):
        self.running = True
        self._loop()

    def _loop(self):
        clock = pygame.time.Clock()
        accumulator = 0.0
        fixed_dt = 1.0 / self.max_tps

        while self.running:
            dt = clock.tick(self.max_fps) / 1000

            accumulator += dt

            while accumulator >= fixed_dt:
                self._update()
                accumulator -= fixed_dt
            
            self._draw()

            self.delta_time = fixed_dt

    def _update(self):
        self._process_input_events()
        self.screen.fill((0, 0, 0))

        scene = self.current_scene
        if not scene.is_started:  
            scene.start(self)
            scene.is_started = True

        scene.update(self)

    def _process_input_events(self):

        for event in pygame.event.get():
    
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                self.input_status.keys[pygame.key.name(event.key)] = True

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
        if self.current_scene.is_started:
            self.current_scene.draw(self)

        scaled = pygame.transform.scale(self.screen, self.window.get_size())
        self.window.blit(scaled, (0,0))

        pygame.display.flip()

@dataclass
class InputStatus:
    keys = {}
    mouse_position = (0,0)
    mouse_buttons = [False] * 5