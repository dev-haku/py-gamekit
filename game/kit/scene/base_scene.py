import pygame


from game.kit.gameobject.worldobject.camera import Camera
from game.kit.component.transform import Transform

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
        if not get_state(camera):
            return

        camera_transform = camera.get_component("Transform")
        if not get_state(camera_transform):
            return
        
        renderers = [
            comp.renderer 
            for wo in self.world 
            if get_state(wo)
            for comp in wo.components 
            if get_state(comp)
            if hasattr(comp, "renderer")
        ]

        renderers.sort(key=lambda x: x.layer)

        for renderer in renderers:

            draw_surface = renderer.surface

            camera_position = camera_transform.position.xy

            draw_position = (
                (renderer.position.x - camera_position.x) + (screen_size[0] // 2),
                (renderer.position.y - camera_position.y) + (screen_size[1] // 2)
            )

            engine.screen.blit(
                draw_surface,
                draw_position
            )

    def _draw_uiobjects(self, engine):

        screen_size = engine.screen.get_size()

        renderers = [
            comp.renderer
            for uo in self.canvas
            if get_state(uo)
            for comp in uo.components
            if get_state(comp)
            if hasattr(comp, "renderer")
        ]

        renderers.sort(key=lambda x: x.layer)
            
        for renderer in renderers:
            draw_surface: pygame.Surface = renderer.surface

            x, y = renderer.position.xy

            w, h = draw_surface.get_size()

            draw_position = (
                (screen_size[0] * x - w // 2),
                (screen_size[1] * y - h // 2)
            )

            engine.screen.blit(draw_surface, draw_position)

def get_state(object):
    if object is None:
        return False
    
    if not object.active:
        return False
    
    return True