""" aggregated total points for a club across different seasons """

import pandas

from epl.common.dataframes import get as get_dataframe
from epl.common.teams import execute as get_teams
from epl.common.scores import execute as cal_scores


def execute():
    """ return aggregated total points for a club across different seasons
    """
    dataframe = get_dataframe("data")
    result = None

    for team in get_teams({}):
        per_team = cal_scores({"dataframe": dataframe, "team": team})
        agg = pandas.DataFrame(
            per_team[["score"]].agg("sum").reset_index(drop=True),
            columns=["sum"],
        )
        agg["team"] = team

        if result is None:
            result = agg
        else:
            result = pandas.concat([result, agg], sort=False).reset_index(
                drop=True
            )
    result.sort_values(by=["sum"], ascending=False, inplace=True)
    return result.reset_index(drop=True)
