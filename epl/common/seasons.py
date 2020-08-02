""" aggregated total points for a club across different seasons """

import numpy

from epl.common.dataframes import get as get_dataframe


def execute(prop: dict = None):
    """ return the seasons. the last N seasons will be return of last in prop
        is provided

    Args:
        prop (dict): prop.

    Returns:
        list: list of str
    """
    if prop is None:
        prop = {}
    dataframe = get_dataframe("data")
    sorted = numpy.sort(dataframe["season"].unique()).tolist()
    if "last" in prop:
        sorted.reverse()
        result = sorted[0 : int(prop["last"])]
        result.reverse()
        return result

    return sorted
