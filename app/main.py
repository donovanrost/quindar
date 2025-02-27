from flask import Flask
from app.api.routes import bp
from app.config import config

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    
    app.register_blueprint(bp, url_prefix='/api')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=config.DEBUG)