""" Microservice """
import os
import json

from flask import Flask, request, render_template
from epl.common.http import bad_req_response, json_response, not_found_req_response
from epl.services.top_clubs import execute as top_clubs
from epl.services.agg_total_points import execute as agg_total_points
from epl.services.agg_wins import execute as agg_wins
from epl.services.agg_goals import execute as agg_goals
from epl.services.matches import execute as matches
from epl.services.referees import execute as referees

APP = Flask(
    __name__,
    static_url_path="",
    template_folder=f"{os.getcwd()}/templates",
    static_folder=f"{os.getcwd()}/static",
)


@APP.route("/")
def index():
    return render_template("index.html")


@APP.route("/map")
def map_index():
    return render_template("map.html")


@APP.route("/table")
def table_index():
    season = request.args.get("s")
    (result, season) = matches({"season": season})
    if len(result) == 0:
        return not_found_req_response("Not Found")
    return render_template("table.html", season=season, matches=result)


@APP.route("/top_clubs")
def top_clubs_index():
    num = request.args.get("n", 5)
    last = request.args.get("l", 5)
    result = top_clubs({"num": int(num), "last": int(last)})
    result = result.to_dict(orient="record")
    return render_template("top_clubs.html", last=last, result=result)


@APP.route("/referees")
def referees_index():
    season = request.args.get("s")
    last = request.args.get("l")
    num = request.args.get("n")
    n_last = int(last) if last is not None else None
    result = referees({"season": season, "last": n_last})
    result = result.to_dict(orient="record")
    result = sorted(result, key=lambda x: (-x["count"]))

    if num is not None:
        result = result[0 : int(num)]

    return render_template("referees.html", result=result)


@APP.route("/api/referees")
def referees_api():
    season = request.args.get("s")
    last = request.args.get("l")
    num = request.args.get("n")

    n_last = int(last) if last is not None else None
    result = referees({"season": season, "last": n_last})
    result = result.to_dict(orient="record")
    result = sorted(result, key=lambda x: (-x["count"]))

    if num is not None:
        result = result[0 : int(num)]
    sum = 0
    for x in result:
        sum = sum + x["count"]
    print(sum)
    return json_response(json.dumps(result))


@APP.route("/api/top_clubs")
def topclubs() -> object:
    """ return list of top clubs
    """
    num = request.args.get("n", 5)
    last = request.args.get("l", 5)
    result = top_clubs({"num": int(num), "last": int(last)})
    return json_response(json.dumps(result.to_dict(orient="record")))


@APP.route("/api/team_scores")
def team_scores() -> object:
    """ return scores of team for each season
    """
    team = request.args.get("t")
    if team is None:
        return bad_req_response("missing t query parameter")
    return json_response(agg_total_points({"team": team}))


@APP.route("/api/team_wins")
def team_wins() -> object:
    """ return number of wins, draws or loses of team for each season
    """
    team = request.args.get("t")
    if team is None:
        return bad_req_response("missing t query parameter")
    last = request.args.get("l", 8)
    return json_response(agg_wins({"team": team, "last": int(last)}))


@APP.route("/api/team_goals")
def team_goals() -> object:
    """ return number of goals scored and conceded of team for each season
    """
    team = request.args.get("t")
    if team is None:
        return bad_req_response("missing t query parameter")
    last = request.args.get("l", 8)
    return json_response(agg_goals({"team": team, "last": int(last)}))


if __name__ == "__main__":
    APP.run(host="0.0.0.0", port=80)
