import models
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///sample.db')
Session = sessionmaker(bind=engine)

models.Base.metadata.drop_all(engine)
models.Base.metadata.create_all(engine)


def store(items):
    s = Session()
    cache = dict()
    for model in items:
        if hasattr(model, 'unique'):
            unique_values = tuple(getattr(model, attr) for attr in model.unique)
            if unique_values in cache:
                model.id = cache[unique_values]
                continue
            modelClass = model.__class__
            query = s.query(modelClass)
            for attr in model.unique:
                query = query.filter(getattr(modelClass, attr) == getattr(model, attr))
            data = query.one_or_none()
            if data:
                cache[unique_values] = data.id
                model.id = data.id
            else:
                s.query(model.__class__)
                s.add(model)
                s.flush()
                cache[unique_values] = model.id
        else:
            s.add(model)
    s.commit()