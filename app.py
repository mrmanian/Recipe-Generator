# Import required packages
import os
from flask import Flask, render_template, request
import twitter
import spoonacular


# List of foods
DESSERTS = ["Ice Cream", "Cake", "Pie", "Cookie", "Brownie", "Pudding", "Macarons"]

# Create new list to use when no tweets are found and empty list when no recipes are found
NO_TWEETS_FOUND = [["No tweets found.", "", "", ""] for _ in range(7)]
EMPTY = ["" for _ in range(16)]

# Index position
INDEX = [-1]

# Create the Flask application
app = Flask(__name__)

# Displays the home page accessible at the addresss '/'
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Get recipe information
        total_results, title, image, food_id = spoonacular.Spoonacular(
            request.form["recipe"], ""
        ).recipe_response()

        # If there are no recipes to display
        if total_results == 0:
            return render_template(
                "home.html",
                title="No recipes found",
                servings=0,
                cook_time="N/A",
                length=len(EMPTY),
                ingredients=EMPTY,
                tweets=NO_TWEETS_FOUND,
                word="",
            )

        (
            source_url,
            servings,
            cook_time,
            short_summary,
            ingredient_list,
        ) = spoonacular.Spoonacular("", food_id).recipe_response2()

        # Get tweets
        tweets = twitter.Twitter(request.form["recipe"] + " -filter:retweets").tweets()

        # If there are less than 7 tweets found
        if len(tweets) < 7:
            return render_template(
                "home.html",
                title=title,
                image=image,
                source_url=source_url,
                servings=servings,
                cook_time=cook_time,
                summary=short_summary,
                length=len(ingredient_list),
                ingredients=ingredient_list,
                tweets=NO_TWEETS_FOUND,
                word=request.form["recipe"].title(),
            )

        # Render the html page
        return render_template(
            "home.html",
            title=title,
            image=image,
            source_url=source_url,
            servings=servings,
            cook_time=cook_time,
            summary=short_summary,
            length=len(ingredient_list),
            ingredients=ingredient_list,
            tweets=tweets,
            word=request.form["recipe"].title(),
        )

    # Index counter to loop through food list
    INDEX[0] += 1
    if INDEX[0] == 7:
        INDEX[0] = 0

    # Get recipe information
    total_results, title, image, food_id = spoonacular.Spoonacular(
        DESSERTS[INDEX[0]], ""
    ).recipe_response()
    (
        source_url,
        servings,
        cook_time,
        short_summary,
        ingredient_list,
    ) = spoonacular.Spoonacular("", food_id).recipe_response2()

    # Get tweets
    tweets = twitter.Twitter(DESSERTS[INDEX[0]] + " -filter:retweets").tweets()

    # Render the html page
    return render_template(
        "home.html",
        title=title,
        image=image,
        source_url=source_url,
        servings=servings,
        cook_time=cook_time,
        summary=short_summary,
        length=len(ingredient_list),
        ingredients=ingredient_list,
        tweets=tweets,
        word=DESSERTS[INDEX[0]],
    )


# Run the application
if __name__ == "__main__":
    app.run(
        debug=True, port=int(os.getenv("PORT", 8080)), host=os.getenv("IP", "0.0.0.0")
    )
