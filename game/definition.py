from .app.game_scene import GameScene


scenes = [
    GameScene,
]

initial_scene_index = 0

global_values = {
    "settings" : None
}

debug = {
    "show_colliders" : False,
    "print_key_events" : False
}