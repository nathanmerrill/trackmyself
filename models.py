from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy.types import *
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import as_declarative, declared_attr

import enum

@as_declarative()
class Base(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower   ()
    id = Column(Integer, primary_key=True)

class Time(object):
    timestamp = Column(DateTime, nullable=False, index=True)

class Name(object):
    unique = ['name']
    name = Column(String, nullable=False, unique=True, index=True)
    
class TransactionType(enum.IntEnum):
    Transfer = 1
    Check = 2
    Debit = 3
    Other = 4


# Models 

class Mood(Base, Name):
    value = Column(Integer, nullable=False, index=True)

class Activity(Base, Name):
    pass

class ActivityItem(Base, Name): #Different types of an activity (aka, which board game)
    activity_id = Column(Integer, ForeignKey('activity.id'), nullable=False, index=True)
    activity = relationship("Activity")

class Location(Base):
    unique = ['lat', 'long']
    name = Column(String, index=True)
    lat = Column(Integer, index=True, nullable=False)
    long = Column(Integer, index=True,  nullable=False)

class Person(Base, Name):
    pass

class Merchant(Base, Name):
    pass

class BankAccount(Base, Name):
    unique = ['bank', 'name']
    bank = Column(String, nullable=False)

class Exercise(Base, Name):
    pass

class Food(Base, Name):
    unique = ['name', 'unit']
    unit = Column(String, nullable=False)
    pass

class Nutrient(Base, Name):
    pass
    
class Track(Base):
    unique = ['name', 'artist', 'album']
    __table_args__ = tuple(UniqueConstraint(*unique, name='uniquetrack'))
    
    name = Column(String, nullable=False, index=True)
    artist = Column(String, nullable=False, index=True)
    album = Column(String, nullable=False, index=True) 
    is_podcast = Column(Boolean, nullable=False,index=True)
    duration = Column(Integer, nullable=False, index=True)
    genre = Column(String, index=True)
    spotify_id = Column(String, index=True)
    danceability = Column(Float, index=True)
    energy = Column(Float, index=True)
    loudness = Column(Float, index=True)
    speechiness = Column(Float, index=True)
    instrumentalness = Column(Float, index=True)
    valence = Column(Float, index=True)   
    tempo = Column(Float, index=True)
    key = Column(Integer, index=True)
    mode = Column(Integer, index=True)
    time_signature = Column(Integer, index=True)

    
class ElectronicActivity(Base, Name):  #The app I'm using, or the domain I've hit
    productivity_score = Column(Integer, nullable=False, index=True)
    category = Column(String, index=True)

class FoodNutrient(Base): #in a single serving
    unique = ['food_id', 'nutrient_id']
    food_id = Column(Integer, ForeignKey('food.id'), nullable=False)
    food = relationship("Food")
    nutrient_id = Column(Integer, ForeignKey('nutrient.id'), nullable=False)
    nutrient = relationship("Nutrient")
    quantity = Column(Float, index=True)

class ChatReciept(Base):
    unique = ['chat_id', 'reciever_id']
    chat_id = Column(Integer, ForeignKey('chathistory.id'), nullable=False)
    reciever_id = Column(Integer, ForeignKey('person.id'), nullable=False)
    

#Time based models
class ListenHistory(Base, Time):
    track_id = Column(Integer, ForeignKey('track.id'), nullable=False)
    track = relationship("Track")
    duration = Column(Integer, nullable=False, index=True)
    
class SleepHistory(Base, Time):
    unique = ['ref_id']
    ref_id = Column(Integer, nullable=False, index=True)
    duration = Column(Integer, nullable=False, index=True)
    stop = Column(DateTime, nullable=False, index=True)
    isNap = Column(Boolean, nullable=False, index=True)
    
class ElectronicActivityHistory(Base, Time):
    activity_id = Column(Integer, ForeignKey('electronicactivity.id'), nullable=False)
    activity = relationship("ElectronicActivity")
    duration = Column(Integer, nullable=False, index=True)
    page_title = Column(String, index=True)
    
class FoodHistory(Base, Time):
    food_id = Column(Integer, ForeignKey('food.id'), nullable=False, index=True)
    food = relationship("Food")
    meal = Column(String, nullable=False, index=True)
    servings = Column(Float, nullable=False, index=True)

class ExerciseHistory(Base, Time):
    exercise_id = Column(Integer, ForeignKey('exercise.id'), nullable=False, index=True)
    exercise = relationship("Exercise")
    duration = Column(Integer, nullable=False, index=True)

class TransactionHistory(Base, Time):
    unique = ['ref_id']
    ref_id = Column(String, nullable=False, index=True, unique=True)
    amount = Column(Integer, nullable=False, index=True)
    merchant_id = Column(Integer, ForeignKey('merchant.id'), nullable=False)
    merchant = relationship("Merchant")
    bank_account_id = Column(Integer, ForeignKey('bankaccount.id'), nullable=False)
    bank_account = relationship("BankAccount")
    category = Column(String, nullable=False, index=True)
    type = Column(Enum(TransactionType), nullable=False, index=True)
    note = Column(Text, index=True)
    
class ChatHistory(Base, Time):
    unique = ['event_id']
    event_id = Column(String, nullable=False, index=True)
    sender_id = Column(Integer, ForeignKey('person.id'), nullable=False)
    sender = relationship("Person")
    message = Column(Text, nullable=False, index=True)

class MoodHistory(Base, Time):
    mood_id = Column(Integer, ForeignKey('mood.id'), nullable=False, index=True)
    mood = relationship("Mood")

class ActivityHistory(Base, Time):
    activity_id = Column(Integer, ForeignKey('activity.id'), nullable=False, index=True)
    activity = relationship("Activity")
    
class LocationHistory(Base, Time):
    location_id = Column(Integer, ForeignKey('location.id'), nullable=False, index=True)
    location = relationship("Location")
    velocity = Column(Integer, nullable=False, index=True)
    duration = Column(Integer, nullable=False, index=True)
