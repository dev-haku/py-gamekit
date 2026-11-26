import subprocess
import sys

commands = [
    [sys.executable, "my_game/main.py"],
    [sys.executable, "build.py"],
]

for command in commands:
    subprocess.run(command, check=True)

print(">>>>>> Tests All Clear <<<<<<")