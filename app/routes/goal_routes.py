from flask import Blueprint, request
from app.models.goal import Goal
from app.routes.route_utilities import create_model, get_models_with_filters, validate_model, update_model, delete_model
from ..db import db


bp = Blueprint("goals_bp", __name__, url_prefix="/goals")


@bp.post("")
def create_goal():
    request_body = request.get_json()

    return create_model(Goal, request_body)


@bp.get("")
def get_all_goals():
    return get_models_with_filters(Goal, request.args)


@bp.get("/<goal_id>")
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    return {"goal": goal.to_dict()}


@bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    return update_model(goal, request_body)

@bp.delete("/<goal_id>")
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return delete_model(goal)