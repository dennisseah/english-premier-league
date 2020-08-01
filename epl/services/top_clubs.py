""" return the top N clubs based on points """

import json
from epl.common.total_points import execute as ttl_points


def execute(prop: dict):
    """ return the top N clubs based on points

    Args:
        prop (dict): properties
    """
    num = prop["num"] if "num" in prop else 8
    last = prop["last"] if "last" in prop else 8
    df = ttl_points({"last": last})
    return json.dumps(df.iloc[0:num].to_dict(orient="record"))
