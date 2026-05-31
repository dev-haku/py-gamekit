from game.paths import PACKAGE_ASSET_DIR
from game.app.game_scene import GameScene

game = {
    "name" : "MyGame",
    "version" : "0.1",
    "icon_image_path" : PACKAGE_ASSET_DIR / "img/icon.ico",
    
    "window_size" : [960,540],
    "screen_size" : [960,540],

    "max_tps" : 30,
    "max_fps" : 1,

    "initial_scene_class" : GameScene,
}
