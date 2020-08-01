""" score calculating functions """
import numpy


def execute(prop: dict):
    """ inserts a new column in dataframe for score.

    Args:
        prop (dict): properties
    """
    dataframe = prop["dataframe"]
    team = prop["team"]
    df = dataframe[
        dataframe["home"].eq(team) | dataframe["away"].eq(team)
    ].reset_index(drop=True)

    df["score"] = numpy.where(
        df["home"].eq(team) & df["home_score"].gt(df["away_score"]), 3, 0,
    )
    df["score"] = numpy.where(
        df["home"].eq(team) & df["home_score"].eq(df["away_score"]),
        1,
        df["score"],
    )
    df["score"] = numpy.where(
        df["away"].eq(team) & df["away_score"].gt(df["home_score"]),
        3,
        df["score"],
    )
    df["score"] = numpy.where(
        df["away"].eq(team) & df["away_score"].eq(df["home_score"]),
        1,
        df["score"],
    )
    return df
