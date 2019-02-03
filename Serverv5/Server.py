import logging
import config
import API
import Cleaner
import matlab.engine

from apscheduler.schedulers.background import BackgroundScheduler


from flask import (
    Flask,
    render_template,
    request
)

# init eninge
eng = matlab.engine.start_matlab("-nojvm")
eng.addpath('scripts')

# Create the application instance

logging.basicConfig(filename='log.log', format="%(asctime)s : %(levelname)s - %(message)s")
app = Flask(__name__, template_folder="static/templates")

# Create URL routing for the application


@app.route('/')
def home():
    """from apscheduler.schedulers.background import BackgroundScheduler

    This function just responds to the browser ULR
    localhost:5000/

    :return:        the rendered template 'home.html'
    """
    return render_template('home.html')


@app.route('/interactive/')
def interactive():
    return render_template('interactive.html')


@app.route('/algorithms/')
def algorithms():
    return render_template('algorithms.html')


@app.route('/algorithms/machine_learning/')
def machine_learning():
    return render_template('machine_learning.html')


@app.route('/algorithms/image_processing/')
def image_processing():
    return render_template('image_processing.html')


@app.route('/algorithms/computer_vision/')
def computer_vision():
    return render_template('computer_vision.html')


@app.route('/api/info/', methods=["GET"])
def api_documentation():
    return render_template('API.html')

# Let API handle API requests

# API documentation


@app.route('/api/documentation/')
def documentation():
    return API.documentation(app)

# Image requests


@app.route('/api/script_names/')
def script_names():
    return API.script_names(app)


@app.route('/api/preset_names/')
def preset_names():
    return API.preset_names(app)


@app.route('/images/presets/<path:filename>')
def preset_image(filename):
    return API.preset_image(app, filename)


@app.route('/images/output/<path:filename>')
def output_image(filename):
    return API.output_image(app, filename)

# Image upload/removal


@app.route('/api/upload_image/', methods=["POST"])
def upload_image():
    return API.upload_image(app, request)


@app.route('/api/remove_image/', methods=['POST'])
def remove_image():
    return API.remove_image(app, request)


# Scripts

@app.route('/api/', methods=["POST"])
def api():
    return API.api(app, request, eng)


# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(Cleaner.run, 'interval', hours=1)
    app.logger.info("cleaner started")

    app.config['UPLOAD_FOLDER'] = config.input_folder
    app.config['MAX_CONTENT_LENGTH'] = config.max_upload_size
    app.run(host='127.0.0.1', port=5000, debug=False)
