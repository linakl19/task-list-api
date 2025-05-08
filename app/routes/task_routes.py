from datetime import datetime
import os
import requests # HTTP library to make a request to Slack API
from flask import Blueprint, Response, request
from app.models.task import Task
from app.routes.route_utilities import  validate_model, get_models_with_filters, create_model, update_model, delete_model
from ..db import db


bp = Blueprint("bp", __name__, url_prefix="/tasks")


@bp.post("")
def create_task():
    request_body = request.get_json()

    return create_model(Task, request_body)


@bp.get("")
def get_all_tasks():
    return get_models_with_filters(Task, request.args)


@bp.get("/<task_id>")
def gets_one_book(task_id):
    task = validate_model(Task, task_id)
    return {"task": task.to_dict()}


@bp.put("/<task_id>")
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()
    # task.title = request_body["title"]
    # task.description = request_body["description"]

    # db.session.commit()

    # return Response(status=204, mimetype="application/json")
    return update_model(task, request_body)


@bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_model(Task, task_id)
    # db.session.delete(task)
    # db.session.commit()

    # return Response(status=204, mimetype="application/json")
    return delete_model(task)


@bp.patch("/<task_id>/mark_complete")
def mark_task_complete(task_id):
    task = validate_model(Task, task_id)
    
    path = "https://slack.com/api/chat.postMessage"
    API_KEY = os.environ.get("API_KEY")

    headers = {"Authorization": f"Bearer {API_KEY}"}
    body ={
        "channel": "task-notifications",
        "text": f"Someone just completed the task {task.title}"
    }

    if not task.completed_at:
        task.completed_at = datetime.now()
        slack_post = requests.post(path, headers=headers, json=body )
    
    db.session.commit()
    return Response(status=204, mimetype="application/json")


@bp.patch("/<task_id>/mark_incomplete")
def mark_task_incomplete(task_id):
    task = validate_model(Task, task_id)
    if task.completed_at:
        task.completed_at = None
    
    db.session.commit()
    return Response(status=204, mimetype="application/json")

