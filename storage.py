from models import Base
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import random
import itertools

engine = create_engine('sqlite:///sample.db')
Session = sessionmaker(bind=engine)

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)


def store(items):
    session = Session()
    cache = dict()
    for model in itertools.chain.from_iterable(map(iterModels, items)):
        saved = fetch(model, cache, session)
        if saved:
            model.id = saved.id
            continue
        save(model, cache, session)
        
def iterModels(model):
    for attr in dir(model):
        if attr.startswith('_'):
            continue
        value = getattr(model, attr)
        if isinstance(value, Base):
            for subModel in iterModels(value):
                yield subModel
            setattr(model, attr+"_id", value.id)
            delattr(model, attr)
    yield model        
    
def getUniqueValues(model):
    if hasattr(model, 'unique'):
        return tuple(getattr(model, attr) for attr in model.unique)
    return None
   
def save(model, cache, session):
    session.add(model)
    session.commit()
    unique_values = getUniqueValues(model)
    if unique_values:
        cache[unique_values] = model

def fetch(model, cache, session):
    unique_values = getUniqueValues(model)
    if not unique_values:
        return None
    if unique_values in cache:
        return cache[unique_values]
    modelClass = model.__class__
    query = session.query(modelClass)
    for attr in model.unique:
        query = query.filter(getattr(modelClass, attr) == getattr(model, attr))
    data = query.one_or_none()
    if data:
        cache[unique_values] = data
    return data