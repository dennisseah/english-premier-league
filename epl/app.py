""" Microservice """
import os

from flask import Flask, request, render_template
from epl.common.http import bad_req_response, json_response
from epl.services.top_clubs import execute as top_clubs
from epl.services.agg_total_points import execute as agg_total_points
from epl.services.agg_wins import execute as agg_wins

APP = Flask(
    __name__,
    static_url_path="",
    template_folder=f"{os.getcwd()}/templates",
    static_folder=f"{os.getcwd()}/static",
)


@APP.route("/")
def index():
    return render_template("index.html")


@APP.route("/top_clubs")
def topclubs() -> object:
    """ return list of top clubs
    """
    num = request.args.get("n", 8)
    last = request.args.get("l", 8)
    return json_response(top_clubs({"num": int(num), "last": int(last)}))


@APP.route("/team_scores")
def team_scores() -> object:
    """ return scores of team for each season
    """
    team = request.args.get("t")
    if team is None:
        return bad_req_response("missing t query parameter")
    return json_response(agg_total_points({"team": team}))


@APP.route("/team_wins")
def team_wins() -> object:
    """ return number of wins, draws or loses of team for each season
    """
    team = request.args.get("t")
    if team is None:
        return bad_req_response("missing t query parameter")
    last = request.args.get("l", 8)
    return json_response(agg_wins({"team": team, "last": int(last)}))


if __name__ == "__main__":
    APP.run(host="0.0.0.0", port=80)
