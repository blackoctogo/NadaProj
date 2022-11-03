
from flask import Flask, render_template, request, redirect, url_for, send_file, session
from datetime import datetime, timedelta
import requests
import random
import string
import flask_restful
from flask_restful import Api
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
CORS(app)


@app.route("/")
def home():

    return render_template('base.html')

@app.context_processor
def utility_processor():
    def pluralize(count, singular, plural=None):
        if not isinstance(count, int):
            raise ValueError('"{}" must be an integer'.format(count))

        if plural is None:
            plural = singular + 's'

        string = singular if count == 1 else plural

        return "{} {}".format(count, string)

    return dict(pluralize=pluralize, now=datetime.now())

















if __name__ != '__main__':
    app.run(debug=True)

