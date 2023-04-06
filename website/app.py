from flask import Flask, render_template, url_for, request, redirct, make_response
import random
import json
from time import time


app = Flask(__name__)

def main():
    return render_template('index.html')

@app.route('/data', methods=["GET", "POST"])
def data():
    Pressure = random.random() * 1000
    Temperature = random.random() * 100
    Humidity = random.random() * 55

    data = [time() * 1000, Pressure, Humidity, Temperature]

    response = make_response(json.dumps(data))

    response.content_type = 'applications/json'

    return response

main()