from flask import Flask, url_for, redirect, request, render_template, jsonify
import requests
from app.services import *

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/countries")
def countries():
    resp = requests.get('http://localhost:5001/countries')
    country_data = []
    for country in resp.json():
        deaths = get_summary_of_category("deaths", country)
        confirmed = get_summary_of_category("confirmed", country)
        recovered = get_summary_of_category("recovered", country)
        data = {'Country': country,
                'Deaths': deaths,
                'Recovered': recovered,
                'Confirmed': confirmed,
                }
        country_data.append(data)
    if resp.status_code != 200:
        # todo ApiError add
        raise KeyError('GET /tasks/ {}'.format(resp.status_code))

    return render_template("countries.html", country_data=country_data)


@app.route("/")
def virus():
    return render_template("virus.html")


if __name__ == '__main__':
    app.run(debug=True)

