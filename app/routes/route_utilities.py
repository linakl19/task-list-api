from flask import abort, make_response, Response
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


def create_model(cls, model_data):
    try:
        new_model = cls.from_dict(model_data)
    except KeyError as error:
        response = {"details": "Invalid data"}
        abort(make_response(response, 400))
    
    db.session.add(new_model)
    db.session.commit()

    return {cls.__name__.lower(): new_model.to_dict()}, 201


def get_models_with_filters(cls, filters=None):
    query = db.select(cls)
    sort = None

    if filters:
        for attribute, value in filters.items():
            if attribute == "sort":
                sort = value
                continue  

            if hasattr(cls, attribute):
                query = query.where(getattr(cls, attribute).ilike(f"%{value}%"))
    
    if sort == "asc":
        query = query.order_by(cls.title.asc())
    elif sort == "desc":
        query = query.order_by(cls.title.desc())
    else:
        query = query.order_by(cls.id) 

    models = db.session.scalars(query)

    return [model.to_dict() for model in models]


def update_model(model, model_data):
    for attribute, value in model_data.items():
        setattr(model, attribute, value)
    
    db.session.commit()

    return Response(status=204, mimetype="application/json")


def delete_model(model):
    db.session.delete(model)
    db.session.commit()

    return Response(status=204, mimetype="application/json")


def validate_multiple_models(cls, id_list):
    """
    Validates that all IDs in the given list exist for the specified model class in one.

    Parameters:
    - cls: model class
    - id_list: list of model ids

    Returns:
    - A list of model instances matching the given IDs.

    Aborts:
    - 400 if any ID is not a valid integer.
    - 404 if one or more IDs are not found in the database.
    """
    
    try:
        id_list = [int(id) for id in id_list]
    except:
        response = {"message": f"One or more {cls.__name__} IDs are not valid integers" }
        abort(make_response(response, 400))
    
    # Query for all models matching the given IDs
    models = db.session.scalars(db.select(cls).where(cls.id.in_(id_list))).all()

    # Query for all models matching the given IDs
    if len(models) != len(set(id_list)):
        found_ids = {model.id for model in models}
        missing_ids = set(id_list) - found_ids

        response = {"message": f"{cls.__name__} IDs not found: {missing_ids}"}
        abort(make_response(response, 404))

    return models