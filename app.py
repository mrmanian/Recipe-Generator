# Import required packages
from flask import Flask, render_template, url_for
from tweepy import OAuthHandler, Cursor, API
from dotenv import load_dotenv
import os
import random
import pytz
import requests
import json

# Create the Flask application
app = Flask(__name__)

# Load the .env file
load_dotenv()

# Setup access to Twitter API and Spoonacular API using keys stored in .env file
auth = OAuthHandler(os.getenv('CONSUMER_API_KEY'), os.getenv('CONSUMER_SECRET'))
auth.set_access_token(os.getenv('ACCESS_TOKEN'), os.getenv('ACCESS_SECRET'))
api = API(auth, wait_on_rate_limit = True)
spoonKey = os.getenv('SPOONACULAR_API_KEY')

# List of foods
dessertList = ['Ice Cream', 'Cake', 'Pie', 'Cookie', 'Brownie', 'Pudding', 'Macarons']

# Global variable
index = -1

# Displays the home page accessible at the addresss '/'
@app.route('/')
def home():
    
    # Index counter to loop through food list
    global index
    index += 1
    if index == 7:
        index = 0
    
    # Get title, image, food id of food
    response = requests.get(f'https://api.spoonacular.com/recipes/complexSearch?apiKey={spoonKey}&type=dessert&sort=random&fillIngredients=true&number=1&titleMatch=' + dessertList[index])
    rep = json.loads(response.text)
    title = rep['results'][0]['title']
    image = rep['results'][0]['image']
    food_id = rep['results'][0]['id']
    
    # Get url, serving size, cook time, and summary of food
    response2 = requests.get(f'https://api.spoonacular.com/recipes/{food_id}/information?apiKey={spoonKey}&includeNutrition=false')
    rep2 = json.loads(response2.text)
    sourceUrl = rep2['sourceUrl']
    servings = rep2['servings']
    cookTime = rep2['readyInMinutes']
    summary = rep2['summary'].replace('<b>', '').replace('</b>', '')
    
    # Condense summary
    split_summary = summary.split('.')
    shortSummary = split_summary[0] + '. ' + split_summary[1] + '. ' + split_summary[2] + '. ' + split_summary[3] + '. ' + split_summary[4] + '. ' + split_summary[5] + '. '

    # Get recipe ingredient details
    ingredient_list = []
    ingredients = rep2['extendedIngredients']
    for i in range(0, len(ingredients)):
        ingredient_list.append(ingredients[i]['measures']['us']['amount'])
        ingredient_list.append(ingredients[i]['measures']['us']['unitLong'])
        ingredient_list.append(ingredients[i]['name'])
        ingredient_list.append(ingredients[i]['image'])

    # Generate random number to pick a random tweet
    num = random.randint(0, 9)

    # Food to search for tweets
    food = dessertList[index] + ' -filter:retweets'
    
    # Create Cursor object and search for tweets
    status = Cursor(api.search,
                    q = food,
                    tweet_mode = 'extended',
                    lang = 'en').items(10)
    
    # Gather tweets and relevant information from status and store into a list
    tweets = [[tweet.full_text, tweet.user.screen_name, tweet.created_at, tweet.id] for tweet in status]

    return render_template(
        'home.html',
        title = title,
        image = image,
        sourceUrl = sourceUrl,
        servings = servings,
        cookTime = cookTime,
        summary = shortSummary,
        length = len(ingredient_list), 
        ingredients = ingredient_list,
        word = dessertList[index],
        text = '"' + tweets[num][0] + '"',
        username = ' -@' + tweets[num][1],
        date_time = tweets[num][2].astimezone(pytz.timezone('US/Eastern')).strftime('%I:%M %p · %b %d, %Y'),
        url = f'https://twitter.com/{tweets[num][1]}/status/{tweets[num][3]}'
    )

# Run the application
if __name__ == '__main__':
    app.run(
        debug = True,
        port = int(os.getenv('PORT', 8080)),
        host = os.getenv('IP', '0.0.0.0')
    )
