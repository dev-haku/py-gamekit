import keyword

from pathlib import Path
from string import Template

from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import choice


SCENE_TEMPLATE = Template("""\
from ${path}package import *

class $class_name(Scene):
    def __init__(self, context):
        super().__init__(context)
""")


GAMEOBJECT_TEMPLATE = Template("""\
from ${path}package import *

class $class_name(Gameobject):
    def __init__(self, context):
        super().__init__(context)
""")


COMPONENT_TEMPLATE = Template("""\
from ${path}package import *

class $class_name(Component):
    def __init__(self, context):
        super().__init__(context)
""")


ROOT = Path(__file__).resolve().parent.parent
APP_ROOT = ROOT / "my_game" / "game" / "app"

TEMPLATES = {
    "GameObject" : GAMEOBJECT_TEMPLATE,
    "Component" : COMPONENT_TEMPLATE,
    "Scene" : SCENE_TEMPLATE,
}


def main():
    result = choice(
        message="Select template:",
        options=[
            (template, name)
            for name, template in TEMPLATES.items()
        ] + [("exit", "Exit")],
        default=GAMEOBJECT_TEMPLATE,
    )

    if result == "exit":
        return

    class_name = prompt("Class name: ")
    file_name = prompt("File name: ")

    if not class_name or not class_name.isidentifier() or keyword.iskeyword(class_name):
        print("Invalid class name.")
        return
    
    
    path = prompt(
        "Output directory: ",
        default="./my_game/game/app/",
    )

    target = (ROOT / path).resolve()

    if not target.is_relative_to(APP_ROOT):
        print("Invalid path.")
        return

    relative = target.relative_to(ROOT / "my_game" / "game")
    import_depth = len(relative.parts)

    content = result.substitute(
        path="." * (import_depth + 1),
        class_name=class_name,
    )

    target.mkdir(parents=True, exist_ok=True)

    output_file = target / f"{file_name}.py"

    if output_file.exists():
        print(f"File already exists: {output_file}")
        return

    output_file.write_text(content, encoding="utf-8")

    print(f"Generated. {output_file}")


if __name__ == "__main__":
    main()
