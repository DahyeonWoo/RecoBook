from flask import Flask

def create_app():
    app = Flask(__name__)
    
    from .blueprints import userinfo, statistics
    app.register_blueprint(userinfo.userinfo_bp)
    app.register_blueprint(statistics.statistics_bp)

    return app