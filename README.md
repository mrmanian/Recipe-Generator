# Recipe Generator
This project dynamically generates recipes and a relevant tweet after every page reload by using Twitter API and Spoonacular API. The web app was created using Flask as the backend framework and HTML/CSS as the frontend to design and style the page contents.

## Table of Contents 

1. [Installation](#installation)
2. [API](#api)
3. [Resolved Issues](#resolved-issues)
4. [Known Problems](#known-problems)
5. [Improvement](#improvement)

## Installation
Prerequisites: 

* Windows, MacOS, or Linux machine.
* [Git Bash](https://git-scm.com/downloads) installed in order to run Git commands.

To run this app, you first need to clone my repo to your local machine and then cd into it by typing the following commands on your terminal.

        git clone https://github.com/NJIT-CS490/project1-mrm54.git
        cd project1-mrm54

I have provided a [requirements.txt](https://github.com/NJIT-CS490/project1-mrm54/blob/master/requirements.txt) file which consists of all the packages that were used (python, flask, jinja2, python-dotenv, pytz, requests, tweepy). Use the package manager [pip](https://pip.pypa.io/en/stable/installing/) to download these packages. Using pip or pip3 both works.

        pip install -r requirements.txt
        (or) pip3 install -r requirements.txt

The screenshot below shows the packages included in the [requirements.txt](https://github.com/NJIT-CS490/project1-mrm54/blob/master/requirements.txt) file.

<img src='https://i.postimg.cc/vHTxZNPy/requirements.jpg' border='0'/>

 In the case you already have most of the packages or prefer to install separately, you can always individually pip install them. For example:

        pip install packagename==version
        (or) pip3 install packagename==version

Once everything is installed and setup, open up the [.env_sample](https://github.com/NJIT-CS490/project1-mrm54/blob/master/.env_sample) file on your preferred IDE. This file is a sample template showing exactly which variables to store your secret keys in. Rename the file to .env and delete the comments that I included once you've read it. More information on getting the API keys are in the next section. The screenshot below gives a visual explanation.

<img src='https://i.postimg.cc/26fbCf0S/addtext-com-MTUw-MTA0-Mjg1-NDg.png' border='0'/>

Run the following command after your keys are stored in a .env file. Make sure you are in the root-level directory.
        
        python app.py
        
If you are using AWS Cloud9, preview the application by clicking preview running application. This should successfully render the HTML!

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

**[Back to top](#recipe-generator)**

## Known Problems

#### Problem #1: When searching for tweets, the searched food is part of the authors username and not in the tweet. It will still display it even through the tweet is irrelevant to the food.
* For example, searching for a tweet with the word 'doughnut' may result in an irrelevant tweet by an author who has the word 'doughnut' in his/her name.
* While this is a rare occasion, it has happened to me a few times. An option to fix this could be to filter out those irrelevant tweets that contain the food in the authors name out of the list and replace it with another tweet.

**[Back to top](#recipe-generator)**

## Improvement

TBD

**[Back to top](#recipe-generator)**
