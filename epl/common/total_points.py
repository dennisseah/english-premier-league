""" aggregated total points for a club across different seasons """

import pandas

from epl.common.dataframes import get as get_dataframe
from epl.common.teams import execute as get_teams
from epl.common.seasons import execute as seasons
from epl.common.scores import execute as cal_scores


def execute(prop: dict = None):
    """ return aggregated total points for a club across different seasons.
        the last N seasons will be return of last in prop
        is provided

    Args:
        prop (dict): prop.

    Returns:
        list: list of object
    """
    if prop is None:
        prop = {}

    dataframe = get_dataframe("data")
    if "last" in prop:
        last_seasons = seasons({"last": prop["last"]})
        dataframe = dataframe[dataframe["season"].isin(last_seasons)]
    result = None

    for team in get_teams({}):
        per_team = cal_scores({"dataframe": dataframe, "team": team})
        agg = pandas.DataFrame(
            per_team[["score"]].agg("sum").reset_index(drop=True), columns=["sum"],
        )
        agg["team"] = team

        if result is None:
            result = agg
        else:
            result = pandas.concat([result, agg], sort=False).reset_index(drop=True)
    result.sort_values(by=["sum"], ascending=False, inplace=True)
    return result.reset_index(drop=True)
