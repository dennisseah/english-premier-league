""" aggregated total points for a club across different seasons """

import json

from epl.common.dataframes import get as get_dataframe
from epl.common.wins import execute as cal_wins


def execute(prop: dict):
    """ return aggregated total points for a club across different seasons

    Args:
        prop (dict): properties
    """
    dataframe = cal_wins(
        {"dataframe": get_dataframe("data"), "team": prop["team"], "last": prop["last"]}
    )
    dataframe_agg = (
        dataframe[["season", "wins", "draws", "loses"]].groupby(["season"]).agg("sum").reset_index()
    )
    return json.dumps(dataframe_agg.to_dict(orient="record"))
