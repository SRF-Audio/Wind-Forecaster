import json

def json_pretty_print(data):
    """
    Convert a Python object into a pretty-printed JSON format string.

    Args:
        data (dict): The Python object to convert.

    Returns:
        str: A string of the Python object in pretty-printed JSON format.
    """
    return json.dumps(data, indent=4)
