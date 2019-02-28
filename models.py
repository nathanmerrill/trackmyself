from sqlalchemy import Column, DateTime, Date, String, Boolean, Decimal, Float, Integer, ForeignKey, Enum
from sqlalchemy.ext.declarative import as_declarative
import enum

@as_declarative()
class Base(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
    id = Column(Integer, primary_key=True)

class TimeBase(Base):
	timestamp = Column(DateTime, nullable=False)

class NameBase(Base):
    name = Column(String, nullable=False)

class MessageSource(enum.IntEnum):
    Self = 1
	Another = 2
	
class TransactionType(enum.IntEnum):
    Transfer = 1
	Check = 2
	Debit = 3
	Other = 4

# Models 

class Mood(NameBase):
	value = Column(Integer, nullable=False)

class Activity(NameBase):
	pass

class ActivityItem(NameBase): #Different types of an activity (aka, which board game)
	activity = Column(Integer, ForeignKey('activity.id'), nullable=False)

class Location(NameBase):
	lat = Column(Integer, nullable=False)
	long = Column(Integer, nullable=False)

class Person(NameBase):
	pass

class Merchant(NameBase):
	pass

class Bank(NameBase):
	alias = Column(String, nullable=False)

class BankAccount(NameBase):
	bank = Column(Integer, ForeignKey('bank.id'), nullable=False)
	alias = Column(String, nullable=False)

class TransactionCategory(NameBase):
	pass	

class Exercise(NameBase):
	pass
	
class Food(NameBase):
	pass

class Nutrient(NameBase):
	unit = Column(String, nullable=False)
	pass

class Meal(NameBase):
	pass
	
class Artist(NameBase):
	isPodcast = Column(Boolean, nullable=False)
	pass

class Album(NameBase):
	artist = Column(Integer, ForeignKey('artist.id'), nullable=False)
	
class Track(NameBase):
	album = Column(Integer, ForeignKey('album.id'), nullable=False)
	duration = Column(Integer, nullable=False)

class ElectronicActivity(NameBase):  #The app I'm using, or the domain I've hit
	productivityScore = Column(Integer, nullable=False)
	category = Column(String)



class FoodNutrient(Base): #in a single serving
	food = Column(Integer, ForeignKey('food.id'), nullable=False)
	nutrient = Column(Integer, ForeignKey('nutrient.id'), nullable=False)

class PersonAlias(Base):
	person = Column(Integer, ForeignKey('person.id'), nullable=False)
	alias = Column(String)

class ChatParticipant(Base):
	chat = Column(Integer, ForeignKey('chathistory.id'), nullable=False)
	person = Column(Integer, ForeignKey('person.id'), nullable=False)
	

#Time based models
class ListenHistory(TimeBase):
	track = Column(Integer, ForeignKey('track.id'), nullable=False)
	duration = Column(Integer, nullable=False)
	trackPercentage = Column(Float, nullable=False)
	
class SleepHistory(TimeBase):
	duration = Column(Integer)
	
class ElectronicActivityHistory(TimeBase):
	activity = Column(Integer, ForeignKey('electronicactivity.id'), nullable=False)
	duration = Column(Integer)
	pageTitle = Column(String)
	url = column(String)
	
class FoodHistory(TimeBase):
	food = Column(Integer, ForeignKey('food.id'), nullable=False)
	meal = Column(Integer, ForeignKey('meal.id'), nullable=False)
	servings = Column(Decimal, nullable=False)

class ExerciseHistory(TimeBase):
	exercise = Column(Integer, ForeignKey('exercise.id'), nullable=False)
	duration = Column(Integer, nullable=False)

class TransactionHistory(TimeBase):
	transactionId = Column(String, nullable=False)
	amount = Column(Decimal, nullable=False)
	merchant = Column(Integer, ForeignKey('merchant.id'), nullable=False)
	bankaccount = Column(Integer, ForeignKey('bankaccount.id'), nullable=False)
	category = Column(Integer, ForeignKey('category.id'), nullable=False)
	type = Column(Enum(TransactionType), nullable=False)
	note = Column(String)
	
class ChatHistory(TimeBase):
	eventId = Column(String, nullable=False) 
	message = Column(Text, nullable=False)
	sender = Column(Enum(MessageSource), nullable=False)

class MoodHistory(TimeBase):
	mood = Column(Integer, ForeignKey('mood.id'), nullable=False)

class ActivityHistory(TimeBase):
	activity = Column(Integer, ForeignKey('activity.id'), nullable=False)
	
class LocationHistory(TimeBase):
	location = Column(Integer, nullable=False)
	velocity = Column(Integer)
