""" returns all referees """

from epl.common.dataframes import get as get_dataframe
from epl.common.seasons import execute as seasons


def execute(prop: dict):
    """ return all teams

    Args:
        prop (dict): properties
    """
    dataframe = get_dataframe("data")
    if "season" in prop and prop["season"] is not None:
        dataframe = dataframe[dataframe["season"].eq(prop["season"])]
    elif "last" in prop and prop["last"] is not None:
        last_seasons = seasons({"last": prop["last"]})
        dataframe = dataframe[dataframe["season"].isin(last_seasons)]

    result = dataframe["referee"].value_counts().reset_index()
    result.columns = ["referee", "count"]
    return result
