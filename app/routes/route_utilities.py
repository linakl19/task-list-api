from datetime import datetime
from flask import abort, make_response
from app.models.task import Task
from ..db import db

def validate_model(cls, model_id):
    try: 
        model_id = int(model_id)
    except:
        response = {"message": f"{cls.__name__} id{model_id} is invalid" }
        abort(make_response(response, 400))
    
    query = db.select(cls).where(cls.id == model_id)
    model = db.session.scalar(query)

    if not model:
        response = {"message": f"{cls.__name__} {model_id} not found"}
        abort(make_response(response, 404))
    
    return model


def create_record(cls, request_body):
    try:
        new_model = cls.from_dict(request_body)

    except KeyError as error:
        response = {"details": "Invalid data"}
        abort(make_response(response, 400))
    
    db.session.add(new_model)
    db.session.commit()
    print(new_model.title)
    return {cls.__name__.lower(): new_model.to_dict()}, 201
    # return new_model.to_dict(), 201


def get_models_with_filters(cls, filters=None):
    query = db.select(cls)

    if filters:
        for attribute, value in filters.items():
            if hasattr(cls, attribute):
                query = query.where(getattr(cls, attribute).ilike(f"%{value}%"))

    models = db.session.scalars(query.order_by(cls.id))
    return [model.to_dict() for model in models]