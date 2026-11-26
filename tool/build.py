import datetime
import pathlib
import subprocess
import sys
import tomllib


ROOT = pathlib.Path(__file__).resolve().parent.parent

with open(ROOT / "my_game" / "game" / "config.toml", "rb") as f:
    config = tomllib.load(f)

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
DIR_NAME = f"v{config['version']}_{timestamp}"

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

print(f"ビルドが完了しました: {BUILD_PATH}")

print("実行ファイルの動作テストを開始します...")

executable = BUILD_PATH / "dist" / config["title"] / config["title"]
subprocess.run([str(executable)], check=True)

print("実行ファイルの動作テストが完了しました。")