""" return matches played per season """

from epl.common.referees import execute as referees


def execute(prop: dict = None):
    """ return matches played per season

    Args:
        prop (dict): properties
    """
    if prop is None:
        prop = {}
    season = prop["season"] if "season" in prop else None
    last = prop["last"] if "last" in prop else None
    refs = referees({"season": season, "last": last})
    return refs
