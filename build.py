import subprocess
from pathlib import Path
import datetime

from game import config


ROOT = Path(__file__).resolve().parent

_name = config.game["name"]
_version = config.game["version"]
_phase = config.game["phase"]

DIR_NAME = datetime.datetime.now().strftime(f"{_name}_v{_version}_{_phase}_%Y%m%d_%H%M%S")

BUILD_ROOT = ROOT / "build" / DIR_NAME
BUILD_ROOT.mkdir(parents=True, exist_ok=True)


# 古い.spec を削除
spec_file = BUILD_ROOT / f"{_name}.spec"
if spec_file.exists():
    spec_file.unlink()

cmd = [
    "pyinstaller",
    "--onedir",
    "--noconsole",
    "--name",        _name,
    "--icon",        str((ROOT / config.game["icon_image_path"]).resolve()),
    "--add-data",    f"{ROOT / 'game/app/asset'};game/app/asset",
    "--add-data",    f"{ROOT / 'game/kit/asset'};game/kit/asset",
    "--distpath",    str(BUILD_ROOT / "dist"),
    "--workpath",    str(BUILD_ROOT / "build"),
    "--specpath",    str(BUILD_ROOT),
    str((ROOT / "run.py").resolve()),
]

subprocess.run(cmd)