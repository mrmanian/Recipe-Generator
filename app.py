from flask import Flask, render_template, url_for
from dotenv import load_dotenv
import os
import random

app = Flask(__name__)
load_dotenv()
 
@app.route('/') # Python decorator

def index():
    return render_template(
        "home.html"
        )

if __name__=='__main__':
    app.run(
        debug = True,
        port = int(os.getenv('PORT', 8080)),
        host = os.getenv('IP', '0.0.0.0')
    )
