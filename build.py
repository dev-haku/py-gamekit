import datetime
import pathlib
import subprocess
import sys
import tomllib

ROOT = pathlib.Path(__file__).resolve().parent

with open(ROOT / "my_game" / "game" / "config.toml", "rb") as f:
    config = tomllib.load(f)

DIR_NAME = datetime.datetime.now().strftime(
    f"v{config["version"]}_%Y%m%d_%H%M%S"
)

BUILD_PATH = ROOT / "build" / DIR_NAME

BUILD_PATH.mkdir(parents=True, exist_ok=True)


SPEC_PATH = ROOT / "game.spec"

cmd = [
    sys.executable,
    "-m",
    "PyInstaller",
    "--noconfirm",
    "--clean",
    "--distpath", str(BUILD_PATH / "dist"),
    "--workpath", str(BUILD_PATH / "work"),
    str(SPEC_PATH),
]

subprocess.run(cmd, check=True)

print(f"Build completed: {BUILD_PATH}")