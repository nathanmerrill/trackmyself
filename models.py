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

class MessageSource(enum.IntEnum):
    Self = 1
    Another = 2
    
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
    activity = Column(Integer, ForeignKey('activity.id'), nullable=False, index=True)

class Location(Base):
    name = Column(String, index=True)
    lat = Column(Integer, nullable=False)
    long = Column(Integer, nullable=False)

class Person(Base, Name):
    pass

class Merchant(Base, Name):
    pass

class Bank(Base, Name):
    alias = Column(String,  nullable=False)

class BankAccount(Base, Name):
    bank = Column(Integer, ForeignKey('bank.id'), nullable=False)
    alias = Column(String, nullable=False)

class TransactionCategory(Base, Name):
    pass    

class Exercise(Base, Name):
    pass
    
class Food(Base, Name):
    pass

class Nutrient(Base, Name):
    unit = Column(String, nullable=False)
    pass

class Meal(Base, Name):
    pass
    
class Track(Base):
    unique = ['name', 'artist', 'album']
    __table_args__ = tuple(UniqueConstraint(*unique, name='uniquetrack'))
    
    name = Column(String, nullable=False, index=True)
    artist = Column(String, nullable=False, index=True)
    album = Column(String, nullable=False, index=True) 
    is_podcast = Column(Boolean, nullable=False, index=True)
    duration = Column(Integer, nullable=False, index=True)

class ElectronicActivity(Base, Name):  #The app I'm using, or the domain I've hit
    productivity_score = Column(Integer, nullable=False, index=True)
    category = Column(String, index=True)



class FoodNutrient(Base): #in a single serving
    food = Column(Integer, ForeignKey('food.id'), nullable=False)
    nutrient = Column(Integer, ForeignKey('nutrient.id'), nullable=False)

class PersonAlias(Base):
    person = Column(Integer, ForeignKey('person.id'), nullable=False)
    alias = Column(String, nullable=False, unique=True, index=True)

class ChatParticipant(Base):
    chat = Column(Integer, ForeignKey('chathistory.id'), nullable=False)
    person = Column(Integer, ForeignKey('person.id'), nullable=False)
    

#Time based models
class ListenHistory(Base, Time):
    track_id = Column(Integer, ForeignKey('track.id'), nullable=False)
    track = relationship("Track")
    listen_duration = Column(Integer, nullable=False, index=True)
    
class SleepHistory(Base, Time):
    duration = Column(Integer, nullable=False, index=True)
    awake_time = Column(DateTime, nullable=False, index=True)
    
class ElectronicActivityHistory(Base, Time):
    activity = Column(Integer, ForeignKey('electronicactivity.id'), nullable=False)
    duration = Column(Integer, nullable=False, index=True)
    page_title = Column(String, nullable=False, index=True)
    url = Column(String, index=True)
    
class FoodHistory(Base, Time):
    food = Column(Integer, ForeignKey('food.id'), nullable=False, index=True)
    meal = Column(Integer, ForeignKey('meal.id'), nullable=False, index=True)
    servings = Column(DECIMAL, nullable=False, index=True)

class ExerciseHistory(Base, Time):
    exercise = Column(Integer, ForeignKey('exercise.id'), nullable=False, index=True)
    duration = Column(Integer, nullable=False, index=True)

class TransactionHistory(Base, Time):
    transaction_id = Column(String, nullable=False, index=True)
    amount = Column(DECIMAL, nullable=False, index=True)
    merchant_id = Column(Integer, ForeignKey('merchant.id'), nullable=False)
    bankaccount_id = Column(Integer, ForeignKey('bankaccount.id'), nullable=False)
    transactioncategory_id = Column(Integer, ForeignKey('transactioncategory.id'), nullable=False)
    type = Column(Enum(TransactionType), nullable=False, index=True)
    note = Column(Text, index=True)
    
class ChatHistory(Base, Time):
    event_id = Column(String, nullable=False, index=True) 
    message = Column(Text, nullable=False, index=True)
    sender = Column(Enum(MessageSource), nullable=False, index=True)

class MoodHistory(Base, Time):
    mood = Column(Integer, ForeignKey('mood.id'), nullable=False, index=True)

class ActivityHistory(Base, Time):
    activity = Column(Integer, ForeignKey('activity.id'), nullable=False, index=True)
    
class LocationHistory(Base, Time):
    location = Column(Integer, nullable=False, index=True)
    velocity = Column(Integer, index=True)
