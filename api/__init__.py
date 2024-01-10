from flask import Flask
from flask_cors import CORS
from api.files import files_api_v1


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    app.register_blueprint(files.files_api_v1)

    @app.route('/')
    def health_check():
        return 'Hey there! Welcome to FileHub.'

    return app
