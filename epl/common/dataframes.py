""" dataframe caches """
import pandas

CACHE = {}


def get(name: str):
    """ return python dataframe

    Args:
        name (str): name of the dataframe

    Returns:
        [type]: pandas dataframe
    """
    if name in CACHE:
        return CACHE[name]
    CACHE[name] = pandas.read_csv(f"data/{name}.csv")
    return CACHE[name]
