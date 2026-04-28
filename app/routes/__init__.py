from flask import Blueprint

# Initialize blueprints here
index_bp = Blueprint('index', __name__)
transaction_bp = Blueprint('transaction', __name__)

# Import the routes to register them with the blueprints
from . import index
from . import transaction_routes

def register_routes(app):
    """
    註冊所有的 blueprints 到 Flask app 中。
    """
    app.register_blueprint(index_bp)
    app.register_blueprint(transaction_bp)
