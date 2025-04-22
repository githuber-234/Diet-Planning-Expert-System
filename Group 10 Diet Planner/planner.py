import random
from data.foods import expanded_foods

def filter_by_restrictions(foods, restrictions):
    if not restrictions:
        return foods
    return [food for food in foods if all(r in food['tags'] for r in restrictions)]

def sort_by_goal(foods, goal):
    if goal == 'Muscle Gain':
        return sorted(foods, key=lambda x: x['protein'], reverse=True)
    elif goal == 'Weight Loss':
        return sorted(foods, key=lambda x: (x['calories'], -x['protein']))
    return foods

def generate_meal_plan(user_data):
    restrictions = user_data.get('diet', [])
    goal = user_data.get('goal', 'Maintenance')
    target_cals = int(user_data.get('calories', 2000))

    allowed_foods = filter_by_restrictions(expanded_foods, restrictions)
    allowed_foods = sort_by_goal(allowed_foods, goal)

    if len(allowed_foods) < 3:
        return {"days": [], "error": "Not enough food options to generate plan."}

    weekly_plan = []
    for _ in range(7):
        day_meals = random.sample(allowed_foods, 3)
        total_cals = sum(meal['calories'] for meal in day_meals)

        weekly_plan.append({
            "meals": day_meals,
            "total_cals": total_cals
        })

    return {"days": weekly_plan}
