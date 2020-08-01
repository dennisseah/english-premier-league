""" returns all teams """
from epl.common.dataframes import get as get_dataframe


def execute(prop: dict):
    """ return all teams

    Args:
        prop (dict): properties
    """
    dataframe = get_dataframe("data")
    if "season" in prop:
        dataframe = dataframe[dataframe["season"].eq(prop["season"])]
    return dataframe["home"].unique().tolist()
