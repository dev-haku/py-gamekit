
# -*- mode: python ; coding: utf-8 -*-

import pathlib
import sys
import yaml
import tomllib


ROOT = pathlib.Path(SPECPATH).resolve()

MY_GAME = ROOT / "my_game"
GAME = MY_GAME / "game"

IS_WINDOWS = sys.platform == "win32"
IS_MACOS = sys.platform == "darwin"


# Load game configuration
with open(GAME /  "config.toml", "rb") as f:
    config = tomllib.load(f)


APP_NAME = config["title"]
VERSION = config["version"]
BUNDLE_IDENTIFIER = config["bundle_identifier"]

ICON_PATH = str(
    (GAME / config["icon_image_path"]).resolve()
)


a = Analysis(
    [str(MY_GAME / "main.py")],

    pathex=[str(MY_GAME)],

    binaries=[],

    datas=[
        (
            str(GAME / "config.toml"),
            "game",
        ),
        (
            str(GAME / "package" / "assets"),
            "game/package/assets",
        ),
        (
            str(GAME / "app" / "assets"),
            "game/app/assets",
        ),
    ],

    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

# PYZ
pyz = PYZ(a.pure)


# Executable
exe = EXE(
    pyz,
    a.scripts,
    [],

    exclude_binaries=True,

    name=APP_NAME,

    debug=False,
    bootloader_ignore_signals=False,

    strip=False,
    upx=True,

    console=False,

    icon=ICON_PATH,
)


# Collect
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,

    strip=False,
    upx=True,

    name=APP_NAME,
)


# macOS Application Bundle
if IS_MACOS:

    app = BUNDLE(
        coll,

        name=f"{APP_NAME}.app",

        icon=ICON_PATH,

        bundle_identifier=BUNDLE_IDENTIFIER,

        info_plist={
            "CFBundleName": APP_NAME,
            "CFBundleDisplayName": APP_NAME,
            "CFBundleShortVersionString": str(VERSION),
        },
    )
