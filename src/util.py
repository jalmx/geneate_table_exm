from pathlib import Path
from os import path


def create_name(path_file: str | Path) -> str:
    """Generate the name file will save gift.txt

    Args:
        path_file (str): path from file to input

    Returns:
        str: new name for the file <name>_gift.txt
    """
    name_full = path.basename(path_file)
    name = path.splitext(name_full)[0]
    name += "_table.html"
    return name
