""" goals calculating functions """
import numpy

from epl.common.dataframes import get as get_dataframe
from epl.common.seasons import execute as seasons


def execute(prop: dict):
    """ inserts a new column in dataframe for goal_scored and goal_conceded.

    Args:
        prop (dict): properties
    """
    dataframe = get_dataframe("data")
    team = prop["team"]

    if "season" in prop:
        dataframe = dataframe[dataframe["season"].eq(prop["season"])]
    elif "last" in prop:
        last_seasons = seasons({"last": prop["last"]})
        dataframe = dataframe[dataframe["season"].isin(last_seasons)]

    df = dataframe[dataframe["home"].eq(team) | dataframe["away"].eq(team)].reset_index(drop=True)
    df["team"] = team
    df["goal_scored"] = 0
    df["goal_conceded"] = 0

    df["goal_scored"] = numpy.where(df["home"].eq(team), df["home_score"], df["goal_scored"],)
    df["goal_scored"] = numpy.where(df["away"].eq(team), df["away_score"], df["goal_scored"],)
    df["goal_conceded"] = numpy.where(df["home"].eq(team), df["away_score"], df["goal_conceded"],)
    df["goal_conceded"] = numpy.where(df["away"].eq(team), df["home_score"], df["goal_conceded"],)

    return df[["season", "team", "goal_scored", "goal_conceded"]]
