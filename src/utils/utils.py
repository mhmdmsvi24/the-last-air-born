import json
import sys
from pathlib import Path

import pygame


def terminate() -> None:
    """Cleanly terminate the game and exit the program."""
    pygame.quit()
    sys.exit()


def load_json(file_path) -> dict:
    """Load and parse a JSON file.

    Args:
        file_path (Path): Path to the JSON file.

    Returns:
        dict: Parsed JSON data.
    """
    with file_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    return data


def deep_copy(data: str) -> dict:
    """Deep copies an object

    Args:
      data (str): dict to copy

    Returns:
      dict
    """
    return json.loads(json.dumps(data))


def update_json_value(
    path: Path, key: str, value: any = None, multiplier: any = None, target: Path = None
):
    """
    Recursively search for a key inside a JSON file and update its value.

    This function loads a JSON document, walks through nested dictionaries,
    and updates the first occurrence of a matching key. The update behavior
    depends on the parameters:

    - If `multiplier` is provided:
        The target value is multiplied:  new_value = old_value * multiplier
    - Else:
        The target value is incremented: new_value = old_value + value

    The modified JSON is written back to the original file unless a
    separate output path (`target`) is specified.

    Args:
        path (Path):
            Path to the JSON file to read and update.

        key (str):
            Name of the key to search for recursively inside the JSON structure.

        value (Any, optional):
            Value to add to the existing value if `multiplier` is not given.
            Defaults to None.

        multiplier (Any, optional):
            Number or factor used to multiply the existing value.
            If provided, it takes precedence over `value`.
            Defaults to None.

        target (Path, optional):
            Optional path to write the updated JSON to instead of overwriting
            the original file. If omitted, `path` will be overwritten.
            Defaults to None.

    Returns:
        bool:
            True if the update succeeded and the file was written.
            False if an error occurred during processing.

    Notes:
        - Only dictionary values are traversed; lists are ignored.
        - Only the first matching key encountered during recursion is updated.
        - The function makes a deep copy of the original JSON data to avoid
          mutating it before writing.
        - Errors during file reading or value modification are caught and
          reported, returning False.
    """

    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    try:

        def recurse(data, key_to_search):
            keys = data.keys()

            if key_to_search in keys:
                if multiplier:
                    data[key_to_search] = data[key_to_search] * multiplier
                else:
                    data[key_to_search] = data[key_to_search] + value
            else:
                for key in keys:
                    if type(data[key]) == dict:
                        recurse(data[key], key_to_search)

            return data

        result = recurse(deep_copy(data), key)
    except Exception as e:
        print(e)
        return False

    if not target:
        with open(path, "w") as f:
            json.dump(result, f, indent=4)
        return True

    with open(target, "w") as f:
        json.dump(result, f, indent=4)

    return True
