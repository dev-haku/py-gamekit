import pygame

from game.package.gameobject.worldobject.camera import Camera


class BaseScene:
    
    def __init__(self):
        self.active = True
        self.is_started = False

        self.world = [] 
        self.canvas = []

        self.camera = self.add_worldobject(Camera())

    def start(self, engine):
        pass

    def update(self, engine):
        for group in (self.world, self.canvas):
            for gameobject in group:
                for component in gameobject.components:
                    if component.is_started == False:
                        component.is_started = True
                        component.start(engine)
                        
                    component.update(engine)

    def draw(self, engine):
        self._draw_worldobjects(engine)
        self._draw_uiobjects(engine)


    def add_worldobject(self, game_object):
        self.world.append(game_object)
        return game_object

    def add_uiobject(self, game_object):
        self.canvas.append(game_object)
        return game_object

    def get_worldobject(self, game_object_name):
        for game_object in self.world:
            if game_object.__class__.__name__ == game_object_name:
                return game_object
            
        return None

    def _draw_worldobjects(self, engine):

        screen_size = engine.screen.get_size()

        camera = self.camera
        if not _get_state(camera):
            return

        camera_transform = camera.get_component("Transform")
        if not _get_state(camera_transform):
            return
        
        render_objects = [
            render_object
            for wo in self.world
            if _get_state(wo)
            if _get_state(wo.get_component("Renderer"))
            for render_object in wo.get_component("Renderer").render_objects.values()
        ]

        render_objects.sort(key=lambda x: x.layer)

        for render in render_objects:

            draw_surface = render.surface

            draw_position = (
                (render.position[0] - camera_transform.position.x) + (screen_size[0] // 2),
                (render.position[1] - camera_transform.position.y) + (screen_size[1] // 2)
            )

            engine.screen.blit(
                draw_surface,
                draw_position
            )

    def _draw_uiobjects(self, engine):

        screen_size = engine.screen.get_size()

        render_objects = [
            render_object
            for uo in self.canvas
            if _get_state(uo)
            if _get_state(uo.get_component("Renderer"))
            for render_object in uo.get_component("Renderer").render_objects.values()
        ]

        render_objects.sort(key=lambda x: x.layer)
            
        for render in render_objects:
            draw_surface: pygame.Surface = render.surface

            position_ratio = render.position
            surface_size = draw_surface.get_size()

            draw_position = (
                (screen_size[0] * position_ratio[0] - surface_size[0] // 2),
                (screen_size[1] * position_ratio[1] - surface_size[1] // 2)
            )

            engine.screen.blit(draw_surface, draw_position)

def _get_state(object):

    if object is None:
        return False
    
    if not object.active:
        return False
    
    return True