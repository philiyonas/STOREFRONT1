""" import random

VARIETIES = {
    "Lettuce": ["Butterhead", "Romaine", "Iceberg", "Oakleaf", "Batavia"],
    "Tomato": ["Cherry", "Beefsteak", "Roma", "Heirloom", "Grape"],
    "Cucumber": ["English", "Persian", "Armenian", "Pickling", "Lemon"],
    "Bell Pepper": ["Red", "Yellow", "Green", "Orange", "Purple"],
    "Strawberry": ["Albion", "Seascape", "Camarosa", "Chandler", "Sweet Charlie"]
}

def generate_random_title():
    category = random.choice(list(VARIETIES.keys()))
    variety = random.choice(VARIETIES[category])
    return f"{variety} {category}" """