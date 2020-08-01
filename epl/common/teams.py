""" returns all teams """
from epl.common.dataframes import get as get_dataframe


def execute(prop: dict):
    """ return all teams

    Args:
        prop (dict): properties
    """
    dataframe = get_dataframe("data")
    return dataframe["home"].unique().tolist()
