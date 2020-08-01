""" return matches played per season """

from epl.common.total_points import execute as ttl_points
from epl.common.wins import execute as ttl_wins
from epl.common.goals import execute as tt_goals


def execute(prop: dict = None):
    """ return matches played per season

    Args:
        prop (dict): properties
    """
    if prop is None:
        prop = {}
    season = prop["season"] if "season" in prop else None

    (df, season) = ttl_points({"last": 1, "season": season})
    if df is None:
        return []

    df = df[df["sum"].gt(0)]
    results = df.to_dict(orient="records")
    mapping = {}
    for result in results:
        mapping[result["team"]] = {"scores": result["sum"]}

    for k in mapping.keys():
        df = ttl_wins({"season": season, "last": 1, "team": k})
        df_agg = df[["team", "wins", "draws", "loses"]].groupby(["team"]).agg("sum").reset_index()
        dic = df_agg.to_dict(orient="records")[0]
        mapping[k]["wins"] = dic["wins"]
        mapping[k]["draws"] = dic["draws"]
        mapping[k]["loses"] = dic["loses"]
        mapping[k]["matches"] = dic["wins"] + dic["draws"] + dic["loses"]

        df = tt_goals({"season": season, "last": 1, "team": k})
        df_agg = (
            df[["team", "goal_scored", "goal_conceded"]].groupby(["team"]).agg("sum").reset_index()
        )
        dic = df_agg.to_dict(orient="records")[0]
        mapping[k]["goal_scored"] = dic["goal_scored"]
        mapping[k]["goal_conceded"] = dic["goal_conceded"]

    results = []
    for k in mapping.keys():
        mapping[k]["team"] = k
        results.append(mapping[k])

    results = sorted(results, key=lambda x: (x["scores"], x["goal_scored"]))
    results.reverse()
    return (results, season)
