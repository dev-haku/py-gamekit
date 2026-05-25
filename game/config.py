from game.app.game_scene import GameScene

game = {
    "name" : "MyGame",
    "version" : "0.1",
    "icon_image_path" : "./game/kit/asset/img/icon.ico",
    
    "window_size" : [800,600],
    "screen_size" : [640,480],

    "max_tps" : 30,
    "max_fps" : 60,

    "initial_scene_class" : GameScene,
}
