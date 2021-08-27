from flask import Flask, render_template, request, jsonify, redirect
import logging
from database import Publication, Author
from controllers import setup_controller, query_controller, raw_controller, topic_app_controller
from queries import mashup

# CREATE THE FLASK APP
application = Flask(__name__, template_folder="templates", static_folder="static")
app = application  # WILL BE REQUIRED TO WORK WHEN WE DEPLOY TO ELASTIC BEANSTALK

# REGISTER CONTROLLERS
app.register_blueprint(setup_controller)
app.register_blueprint(query_controller)
app.register_blueprint(raw_controller)
app.register_blueprint(topic_app_controller)

# CONFIGURE THE APP
app.logger.setLevel(logging.INFO)
with app.app_context():
    app.logger.info(f'Running!')


@app.route('/')
def home():
    # THE MAIN APPLICATION ROUTE
    return redirect('/app')

@app.route("/index")
def index():
    return render_template('index.html.jinja2')

# PREVENT CACHING
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

with app.app_context():
    pass

if __name__ == '__main__':
    app.run()
