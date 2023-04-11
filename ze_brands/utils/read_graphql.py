# Standard Libraries
import os

BASE_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), "../.."))

PROJECT_ROOT = BASE_DIR


def read_graphql(path_file) -> str:
    """
    Reads a GraphQL file and returns its contents as a string.

    Args:
        path_file (str): The file path relative to the project root.

    Returns:
        str: The contents of the GraphQL file.

    Raises:
        FileNotFoundError: If the specified file does not exist.

    """
    _dir = PROJECT_ROOT + path_file
    with open(_dir, "r") as _file:
        data = _file.read()
    return data
