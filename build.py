import os
import sys
import subprocess
import datetime
import pathlib

from game import config
from game import paths

ROOT = pathlib.Path(__file__).resolve().parent

DIR_NAME = datetime.datetime.now().strftime(
    f"v{config.VERSION}_%Y%m%d_%H%M%S"
)

BUILD_PATH = ROOT / "build" / DIR_NAME
BUILD_PATH.mkdir(parents=True, exist_ok=True)

cmd = [
    sys.executable, "-m", "PyInstaller",
    "--onedir",
    "--contents-directory", ".",
    "--windowed",
    "--name",        config.NAME,
    "--icon",        str(config.ICON_IMAGE_PATH.resolve()),
    "--add-data",    f'{paths.ROOT / "package" / "assets"}{os.pathsep}game/package/assets',
    "--add-data",    f'{paths.APP_ASSET_DIR }{os.pathsep}game/app/assets',
    "--distpath",    str(BUILD_PATH / "dist"),
    "--workpath",    str(BUILD_PATH / "build"),
    "--specpath",    str(BUILD_PATH),
    str(ROOT / "run.py"),
]

subprocess.run(cmd, check=True)