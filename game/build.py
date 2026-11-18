import os
import sys
import subprocess
import datetime
import pathlib

from src import config, paths


DIR_NAME = datetime.datetime.now().strftime(f"v{config.VERSION}_%Y%m%d_%H%M%S")

BUILD_ROOT = pathlib.Path(__file__).resolve().parent.parent / "build" / DIR_NAME
BUILD_ROOT.mkdir(parents=True, exist_ok=True)

spec_file = BUILD_ROOT / f"{config.NAME}.spec"
if spec_file.exists():
    spec_file.unlink()

sep = os.pathsep  # Windows: ";"  /  Mac・Linux: ":"

cmd = [
    sys.executable, "-m", "PyInstaller",
    "--onedir",
    "--contents-directory", ".",
    "--windowed",
    "--name",        config.NAME,
    "--icon",        str((paths.ROOT / config.ICON_IMAGE_PATH).resolve()),
    "--add-data",    f"{paths.ROOT / 'assets'}{sep}assets",
    "--distpath",    str(BUILD_ROOT / "dist"),
    "--workpath",    str(BUILD_ROOT / "build"),
    "--specpath",    str(BUILD_ROOT),
    str((paths.ROOT / "main.py").resolve()),
]

subprocess.run(cmd)