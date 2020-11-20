# Import required packages
import os
import json
from dotenv import load_dotenv
import requests

# Load the .env file
load_dotenv()

# Setup access to Spoonacular API using keys stored in .env file
spoonKey = os.getenv("SPOONACULAR_API_KEY")


class Spoonacular:
    def __init__(self, food, food_id):
        self.food = food
        self.food_id = food_id

    # Get title, image, and id of food
    def recipe_response(self):
        food = self.food

        response = requests.get(
            f"https://api.spoonacular.com/recipes/complexSearch?apiKey={spoonKey}&sort=random&fillIngredients=true&number=1&titleMatch="
            + food
        )
        rep = json.loads(response.text)

        if rep["totalResults"] == 0:
            return 0, "", "", ""

        title = rep["results"][0]["title"]
        image = rep["results"][0]["image"]
        food_id = rep["results"][0]["id"]

        return "", title, image, food_id

    # Get url, serving size, cook time, summary, and ingredients of food
    def recipe_response2(self):
        food_id = self.food_id

        response2 = requests.get(
            f"https://api.spoonacular.com/recipes/{food_id}/information?apiKey={spoonKey}&includeNutrition=false"
        )
        rep2 = json.loads(response2.text)

        source_url = rep2["sourceUrl"]
        servings = rep2["servings"]
        cook_time = rep2["readyInMinutes"]
        summary = rep2["summary"].replace("<b>", "").replace("</b>", "")

        # Condense summary
        split_summary = summary.split(".")
        short_summary = (
            split_summary[0]
            + ". "
            + split_summary[1]
            + ". "
            + split_summary[2]
            + ". "
            + split_summary[3]
            + ". "
            + split_summary[4]
            + ". "
            + split_summary[5]
            + ". "
        )

        # Store ingredient measures, name, and image in list
        ingredient_list = []
        ingredients = rep2["extendedIngredients"]
        for i in range(0, len(ingredients)):
            ingredient_list.append(ingredients[i]["measures"]["us"]["amount"])
            ingredient_list.append(ingredients[i]["measures"]["us"]["unitLong"])
            ingredient_list.append(ingredients[i]["name"])
            ingredient_list.append(ingredients[i]["image"])

        return source_url, servings, cook_time, short_summary, ingredient_list
