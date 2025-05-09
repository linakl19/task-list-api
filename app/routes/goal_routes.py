from flask import Blueprint, request
from app.models.goal import Goal
from app.models.task import Task
from app.routes.route_utilities import create_model, get_models_with_filters, validate_model, update_model, delete_model, validate_multiple_models
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


# Nested Routes: One goal(parent) to many tasks(child)
@bp.get("/<goal_id>/tasks")
def get_tasks_by_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    return dict(
        id = goal.id,
        title = goal.title,
        tasks = [task.to_dict() for task in goal.tasks]
    )


@bp.post("/<goal_id>/tasks")
def assign_tasks_to_goal(goal_id):
    """
    Associates the given task IDs with a goal by its ID, and unlinks any previously associated tasks not in the list.

    Validates all task IDs and updates the database accordingly. Returns the goal ID and the updated list of task IDs.

    Request: { "task_ids": [1, 2, 3] }
    Response: { "id": 1, "task_ids": [1, 2, 3] }
    """
    
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    task_ids = request_body.get("task_ids", [])

    # Validate list taks ids in one query to db
    valid_tasks = validate_multiple_models(Task, task_ids)

    # Unlink tasks that are no longer assigned to this goal
    for task_in_goal in goal.tasks:
        if task_in_goal.id not in task_ids:
            task_in_goal.goal_id = None

    valid_tasks_ids = []

    # Assign valid tasks to this goal
    for task in valid_tasks:
        valid_tasks_ids.append(task.id)
        if task.goal_id != goal.id:
            task.goal_id = goal.id

    db.session.commit()

    return {
        "id": goal.id,
        "task_ids": valid_tasks_ids
    }
