from flask import Flask

def create_app():
    app = Flask(__name__)
    
    from .blueprints import userinfo
    app.register_blueprint(userinfo.bp)

    return app