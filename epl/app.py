""" Microservice """
from flask import Flask, request
from epl.common.http import bad_req_response, json_response
from epl.services.top_clubs import execute as top_clubs
from epl.services.agg_total_points import execute as agg_total_points


APP = Flask(__name__)


@APP.route("/top_clubs")
def topclubs() -> object:
    """ return list of top clubs
    """
    return json_response(top_clubs({"num": int(request.args.get("n", "8"))}))


@APP.route("/team_scores")
def team_scores() -> object:
    """ return scores of team for each season
    """
    team = request.args.get("t")
    if team is None:
        return bad_req_response("missing t query parameter")
    return json_response(agg_total_points({"team": team}))


if __name__ == "__main__":
    APP.run(host="0.0.0.0", port=80)
