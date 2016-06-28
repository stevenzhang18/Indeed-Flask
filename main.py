"""`main` is the top level module for your Flask application."""

# Import the Flask Framework
from flask import Flask, render_template, request
#import pandas as pd
app = Flask(__name__)
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.


@app.route('/')
def hello():
    return render_template("main.html")

@app.route('/results', methods=['POST'])
def my_form_post():

    text = request.form['text']
    # processed_text = text.upper()
    # return processed_text
    #cities= masterFunction(text)
    #return render_template("results.html", city1=cities["1"], city2=cities["2"], city3=cities["3"], city4=cities["4"], city5=cities["5"], city6=cities["6"], city7=cities["7"], city8=cities["8"], city9=cities["9"], city10=cities["10"])
    return render_template("results.html", text=text, city2="Omaha, Nebraska", city3="Omaha, Nebraska", city4="Omaha, Nebraska", city5="Omaha, Nebraska", city6="Omaha, Nebraska", city7="Omaha, Nebraska", city8="Omaha, Nebraska", city9="Omaha, Nebraska", city10="Omaha, Nebraska")



@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500
