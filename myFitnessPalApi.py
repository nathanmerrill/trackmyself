import datetime
import myfitnesspal
from models import Food, FoodHistory, Nutrient, FoodNutrient

days = dict()

def apiCall(request, start, end, attribute, timeout):
    client = myfitnesspal.Client(request['username'], request['password'])
    dayCount = (end - start).days + 1
    date = start.date()
    emptyDays = 0
    for i in reversed(range(dayCount)):
        timestamp = date + datetime.timedelta(days=i)
        if timestamp in days:
            day = days[timestamp]
        else:
            day = client.get_date(timestamp)
        items = getattr(day, attribute)
        if all(len(item) == 0 for item in items):
            emptyDays += 1
            if emptyDays == timeout:
                return
            continue
        else:
            emptyDays = 0
        for item in items:
            yield (timestamp, item)

def call(request, start, end):
    for timestamp, meal in apiCall(request, start, end, "meals", 7):
        for i, entry in enumerate(meal.entries):
            food = Food(name=entry.short_name, unit=entry.unit)
            food_quantity=float(entry.quantity)
            yield food
            for name, quantity in entry.totals.items():
                nutrient = Nutrient(name=name)
                yield nutrient
                yield FoodNutrient(food_id=food.id, nutrient_id=nutrient.id, quantity=quantity/food_quantity)     
            yield FoodHistory(timestamp=timestamp, food_id=food.id, meal=meal.name, servings=food_quantity)