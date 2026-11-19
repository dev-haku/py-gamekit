# NOTE:
# Keep this import for pygbag build.
# In some environments, the build did not work when pygame was not imported in main.py.
import pygame

from .package.core.engine import Engine


async def main():
    e = Engine()
    await e.start()