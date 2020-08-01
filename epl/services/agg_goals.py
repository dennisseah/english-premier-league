""" aggregated goals for a club across different seasons """

import json

from epl.common.goals import execute as cal_goals


def execute(prop: dict):
    """ return aggregated goals for a club across different seasons

    Args:
        prop (dict): properties
    """
    dataframe = cal_goals({"team": prop["team"], "last": prop["last"]})
    dataframe_agg = (
        dataframe[["season", "goal_scored", "goal_conceded"]]
        .groupby(["season"])
        .agg("sum")
        .reset_index()
    )
    return json.dumps(dataframe_agg.to_dict(orient="record"))
