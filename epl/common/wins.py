""" wins calculating functions """
import numpy

from epl.common.dataframes import get as get_dataframe
from epl.common.seasons import execute as seasons


def execute(prop: dict):
    """ inserts a new column in dataframe for wins, draws and loses.

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
    df["wins"] = 0
    df["draws"] = 0
    df["loses"] = 0

    df["wins"] = numpy.where(
        df["home"].eq(team) & df["home_score"].gt(df["away_score"]), 1, df["wins"],
    )
    df["draws"] = numpy.where(
        df["home"].eq(team) & df["home_score"].eq(df["away_score"]), 1, df["draws"],
    )
    df["loses"] = numpy.where(
        df["home"].eq(team) & df["home_score"].lt(df["away_score"]), 1, df["loses"],
    )
    df["wins"] = numpy.where(
        df["away"].eq(team) & df["away_score"].gt(df["home_score"]), 1, df["wins"],
    )
    df["draws"] = numpy.where(
        df["away"].eq(team) & df["away_score"].eq(df["home_score"]), 1, df["draws"],
    )
    df["loses"] = numpy.where(
        df["away"].eq(team) & df["away_score"].lt(df["home_score"]), 1, df["loses"],
    )
    return df[["season", "team", "wins", "draws", "loses"]]
