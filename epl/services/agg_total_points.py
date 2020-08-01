""" aggregated total points for a club across different seasons """

import json

from epl.common.dataframes import get as get_dataframe
from epl.common.scores import execute as cal_scores


def execute(prop: dict):
    """ return aggregated total points for a club across different seasons

    Args:
        prop (dict): properties
    """
    dataframe = cal_scores(
        {"dataframe": get_dataframe("data"), "team": prop["team"]}
    )
    dataframe_agg = (
        dataframe[["season", "score"]]
        .groupby(["season"])
        .agg("sum")
        .reset_index()
    )
    return json.dumps(dataframe_agg.to_dict(orient="record"))
