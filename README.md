# Recipe Generator
This project dynamically generates recipes and a relevant tweet after every page reload by using Twitter API and Spoonacular API. The web app was created using Flask as the backend framework and HTML/CSS/Boostrap/JQuery as the frontend to design and style the page contents.

## Table of Contents 

1. [Installation](#installation)
2. [API](#api)
3. [Resolved Issues](#resolved-issues)
4. [Known Problems](#known-problems)
5. [Improvement](#improvement)
6. [Final Remarks](#final-remarks)

## Installation
Prerequisites: 

* Windows, MacOS, or Linux machine.
* [Git Bash](https://git-scm.com/downloads) installed in order to run Git commands.
* [Python](https://www.python.org/downloads/) installed in your system/virtual environment.

To run this app, you first need to clone my repo to your local machine and then cd into it by typing the following commands on your terminal.

        git clone https://github.com/NJIT-CS490/project1-mrm54.git
        cd project1-mrm54

I have provided a [requirements.txt](https://github.com/NJIT-CS490/project1-mrm54/blob/master/requirements.txt) file which consists of all the packages that were used (python, flask, jinja2, python-dotenv, pytz, requests, tweepy). Use the package manager [pip](https://pip.pypa.io/en/stable/installing/) to download these packages. Using pip or pip3 both works.

        pip install -r requirements.txt
        (or) pip3 install -r requirements.txt

The screenshot below shows the packages included in the [requirements.txt](https://github.com/NJIT-CS490/project1-mrm54/blob/master/requirements.txt) file.

<img src='https://i.postimg.cc/CKgDk9nM/requirements.jpg' border='0'/>

 In the case you already have most of the packages or prefer to install separately, you can always individually pip install them. For example:

        pip install packagename==version
        (or) pip3 install packagename==version

Once everything is installed and setup, open up the [.env_sample](https://github.com/NJIT-CS490/project1-mrm54/blob/master/.env_sample) file on your preferred IDE. This file is a sample template showing exactly which variables to store your secret keys in. Rename the file to .env and delete the comments that I included once you've read it. More information on getting the API keys are in the next section. The screenshot below gives a visual explanation.

<img src='https://i.postimg.cc/26fbCf0S/addtext-com-MTUw-MTA0-Mjg1-NDg.png' border='0'/>

Run the following command after your keys are stored in a .env file. Make sure you are in the root-level directory.
        
        python app.py
        
If you are using AWS Cloud9, preview the application by clicking preview running application. This should successfully render the HTML!

Once the code successfully runs locally, now we can deploy it for the world to see! We will be using Heroku to deploy. Sign up for an account [here.](https://dashboard.heroku.com/apps) Once the signup process is complete, we need to install Heroku on your system, so in your terminal type the following command. Note that this might take some time to fully install.

        npm install -g heroku

Next go through the following steps to create an app on Heroku.

        heroku login -i
        heroku create <your-app-name>

Once that is complete, navigate to [this](https://dashboard.heroku.com/apps) website and click on your newly created app. Click on Settings, then scroll to "Config Vars." Click "Reveal Config Vars" and add the key value pairs for each variable. These are the keys in the .env file. It is important to make sure the key names are exactly the same as the .env file other wise the application won't run!

Now we can push the code to Heroku so that it can be deployed. The following command will do precisely that.

        git push heroku master

If all went correctly, the website should be up and running!! In case it does not load properly, you can debug it by running the following command on your console.

        heroku logs --tail

**[Back to top](#recipe-generator)**

## API
#### Twitter API
* Sign up for a developer account [here.](https://developer.twitter.com/en/apply-for-access)

* After signing up, navigate to [this](https://developer.twitter.com/en/portal/projects-and-apps) page and make a new app. You should then get a consumer API key, consumer secret key, access token, and an access secret key. Make note of these keys and store them in the .env file.

#### Spoonacular API
* Sign up for an account [here.](https://spoonacular.com/)

* After signing up, navigate to your [profile](https://spoonacular.com/food-api/console#Profile) and you will see an API key. Make note of this key and store it in the .env file.

**[Back to top](#recipe-generator)**

## Resolved Issues

#### Issue #1: Some of the tweets pulled by Tweepy was truncated.

* Resolved by adding the tweet_mode parameter and setting it to extended to the Cursor object. [This](https://tweepy2.readthedocs.io/en/latest/cursor_tutorial.html) website helped me figure out the solution.

        tweet_mode = 'extended'

#### Issue #2: The date and time of each tweet was not in Eastern Standard Time.

* Through reading the Twitter [documentation,](https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/overview/tweet-object) I found out that .created_at outputs the time in UTC. So to resolve this I installed and imported the pytz package which allowed me to convert the datetime object to EST. I've listed an example snippet below for an arbitrary datetime object obj.

        import pytz
        obj.astimezone(pytz.timezone('US/Eastern'))

#### Issue #3: When pulling ingredient images from spoonacular, sometimes an image does not exist and an ugly broken image square appears on the page.

* I found out through [this](https://stackoverflow.com/questions/7995080/html-if-image-is-not-found) website that I can fix this by showing another image if the main image is not found.

        onerror="this.onerror=null; this.src='https://spoonacular.com/cdn/ingredients_100x100/no.jpg'"

#### Issue #4: A 'confirm form resubmission' alert appeared when clicking reload after using the search bar to search for a recipe.

* This kept happening because after searching for a recipe, the website switches to the POST method so refreshing it will attempt to resubmit the previous search. I resolved this by using Javascript/JQuery to 'change' the history back to the default '/' home page when clicking the refresh button. While this is a 'hacky' way, it got the job done.

        history.pushState(null, "", "/");

**[Back to top](#recipe-generator)**

## Known Problems

#### Problem #1: When searching for tweets, the searched food is part of the authors username and not in the tweet. It will still display it even through the tweet is irrelevant to the food.
* For example, searching for a tweet with the word 'doughnut' may result in an irrelevant tweet by an author who has the word 'doughnut' in his/her name.
* While this is a rare occasion, it has happened to me a few times. An option to fix this could be to filter out those irrelevant tweets that contain the food in the authors name out of the list and replace it with another tweet.

#### Problem #2: Slight rounding errors happen when calculating the ingredient proportions for different serving sizes.
* To start off with, you can only increment the serving size up or down by 1 in my app. I have not customized it so that the user can type a desired number and have it display the appropriate values. I used [this](https://ecampusontario.pressbooks.pub/basickitchenandfoodservicemanagement/chapter/convert-and-adjust-recipes-and-formulas/) website to figure out the formula to calculate the appropriate proportions for different serving sizes.
* There is a slight rounding error when performing this especially when increasing/decreasing the value fast. An option to fix this would be to remove the incremental feature all together and just have the user manually type the number of servings. That way the app won't have to worry about constantly updating the numbers so it should minimize rounding errors. 

**[Back to top](#recipe-generator)**

## Improvement

#### Improvement #1: Autofill search with suggestions based on what the user types in the search bar.

* I started implementing this feature, but due to lack of time decided to scratch it. I was thinking about creating a list filled with a bunch of foods and then using Javascript/JQuery to compare what the user is typing in the search box letter by letter to the list and displaying 6 or 7 suggestions underneath the search bar.

**[Back to top](#recipe-generator)**

## Final Remarks

Please feel free to let me know if any issues arise via the issues tab on Github. Also, if there is a huge feature that would be beneficial to add feel free to clone the repo and try to implement it or let me know so I can also attempt to add it and update the repository!

**[Back to top](#recipe-generator)**
