from pygame import Vector2
from game.kit.gameobject.worldobject.camera import Camera

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
        self.draw_worldobjects(engine)
        self.draw_uiobjects(engine)

    def draw_worldobjects(self, engine):

        for gameobject in self.world:
            
            if gameobject is None:
                print("Noneがworldに入ってる。")
                continue

            camera = self.camera
            if camera is None:
                print("cameraがNone")
                continue
                
            if (
                not gameobject.active and
                not camera.active
                ):
                continue

            gameobject_sprite = gameobject.get_component("Sprite")
            gameobject_transform = gameobject.get_component("Transform")
            camera_transform = camera.get_component("Transform")
            if (
                gameobject_sprite is None or
                gameobject_transform is None or
                camera_transform is None 
                ):
                continue

            if (
                not gameobject_sprite.active and
                not gameobject_transform.active and
                not camera_transform.active 
                ):
                continue

            gameobject_surface = gameobject_sprite.surface
            if gameobject_surface is None:
                continue

            gameobject_position = gameobject_transform.position.xy
            camera_position = camera_transform.position.xy
            
            screen_size = engine.screen.get_size()

            draw_position = (
                (gameobject_position.x - camera_position.x) + (screen_size[0] // 2),
                (gameobject_position.y - camera_position.y) + (screen_size[1] // 2)
            )

            engine.screen.blit(gameobject_surface, draw_position)

    def draw_uiobjects(self, engine):

        for gameobject in self.canvas:
            
            if gameobject is None:
                print("Noneがworldに入ってる。")
                continue
                
            if not gameobject.active:
                continue

            gameobject_image = gameobject.get_component("Image")
            gameobject_recttransform = gameobject.get_component("RectTransform")
            if (
                gameobject_image is None or
                gameobject_recttransform is None
                ):
                continue

            if (
                not gameobject_image.active and
                not gameobject_recttransform.active
                ):
                continue

            gameobject_surface = gameobject_image.get_surface()
            if gameobject_surface is None:
                continue

            position: Vector2 = gameobject_recttransform.position
            scaled_size: Vector2 = gameobject_recttransform.scaled_size
            
            screen_size = engine.screen.get_size()

            print(scaled_size)
            draw_position = (
                (screen_size[0] * position.x) - scaled_size.x // 2,
                (screen_size[1] * position.y) - scaled_size.y // 2
            )

            engine.screen.blit(gameobject_surface, draw_position)


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
