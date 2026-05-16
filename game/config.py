from game.app.main_scene import MainScene

game = {
    "name" : "MyGame",
    "phase" : "pre-alpha",
    "version" : "0.1",
    "icon_image_path" : "./game/kit/asset/img/icon.ico",

    "init_scene_class" : MainScene,

    "tps" : 30,
    "window_size" : [800,600],
    "screen_size" : [640,480],
    "fps" : 60
}
