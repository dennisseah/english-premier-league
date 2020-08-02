""" return the top N clubs based on points """

from epl.common.total_points import execute as ttl_points


def execute(prop: dict):
    """ return the top N clubs based on points

    Args:
        prop (dict): properties
    """
    num = prop["num"] if "num" in prop else 5
    last = prop["last"] if "last" in prop else 5
    (df, _0) = ttl_points({"last": last})
    return df.iloc[0:num]
