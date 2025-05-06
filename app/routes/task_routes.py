from flask import Blueprint, Response, request
from app.models.task import Task
from app.routes.route_utilities import  validate_model, get_models_with_filters, create_record
from ..db import db


bp = Blueprint("bp", __name__, url_prefix="/tasks")


# POST one
@bp.post("")
def create_task():
    request_body = request.get_json()

    return create_record(Task, request_body)


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
    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return Response(status=204, mimetype="application/json")


@bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_model(Task, task_id)
    db.session.delete(task)
    db.session.commit()

    return Response(status=204, mimetype="application/json")