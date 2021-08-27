from flask import Flask, request, jsonify
import logging
from solve import run as run_service_composition
from solve import ServiceComposition
from typing import *

# INITIALIZE THE FLASK APP
application = Flask(__name__)
app = application # REQUIRED FOR EBS FOR SOME REASON

# CONFIG THE APP
app.logger.setLevel(logging.INFO)
with app.app_context():
    app.logger.info(f'Running!')

# PREVENT CACHING IN BROWSER :)
@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


@app.route('/')
def home():
    return "hello, world", 200

@app.route('/service-composition', methods=['GET', 'POST'])
def sevice_composition():

    sc: ServiceComposition
    # CHECK TO SEE IF WEIGHTS ARE CUSTOMIZED
    data: Dict = request.get_json()
    if data is not None:
        print(data)
        cost_weight: float = float(data.get('cost_weight', 0))
        reliability_weight: float = float(data.get('reliability_weight', 0))
        performance_weight: float = float(data.get('performance_weight', 0))
        availability_weight: float = float(data.get('availability_weight', 0))

        total_weight = cost_weight + reliability_weight + performance_weight + availability_weight
        if not total_weight == 1:
            return jsonify(error=f'The sum of your weights must be 1! Instead it is {total_weight}'), 400
        sc = run_service_composition('Data_saved_3.csv', [
            cost_weight,
            reliability_weight,
            performance_weight,
            availability_weight
        ])
    else:
        sc = run_service_composition('Data_saved_3.csv')

    return jsonify(sc.__dict__), 200