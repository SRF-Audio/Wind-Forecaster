import json
from bson.objectid import ObjectId

def json_pretty_print(data):
    """
    Convert a Python object into a pretty-printed JSON format string. This function 
    can handle MongoDB ObjectId fields by converting them to their string representation.

    Args:
        data (dict): The Python object to convert.

    Returns:
        str: A string of the Python object in pretty-printed JSON format.
    """
    class JSONEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, ObjectId):
                return str(o)
            return super().default(o)

    return json.dumps(data, indent=4, cls=JSONEncoder)
