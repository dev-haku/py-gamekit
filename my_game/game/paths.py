from pathlib import Path

ROOT = Path(__file__).resolve().parent

CONFIG_FILE = ROOT / "config.yaml"

DEFAULT_ICON_IMAGE = ROOT / "package" / "assets" / "image" / "default_icon.ico"
CB_IMAGE = ROOT / "package" / "assets" / "image" / "cb.jpg"

APP_ASSET_DIR = ROOT / "app" / "assets"