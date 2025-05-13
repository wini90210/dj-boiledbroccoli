import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
# Corrected import for db, and import all models to ensure they are registered with SQLAlchemy
from src.models import db
from src.models.user import User
from src.models.dietary_preference import DietaryPreference
from src.models.meal_history import MealHistory
from src.models.restaurant import Restaurant

# Import all blueprints
from src.routes.user_routes import user_bp
from src.routes.dietary_preference_routes import preference_bp
from src.routes.meal_history_routes import meal_history_bp
from src.routes.restaurant_routes import restaurant_bp
from src.routes.recommendation_routes import recommendation_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT' # Replace with a strong, unique secret key in production

# Database Configuration - Uncommented and configured
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('DB_USERNAME', 'root')}:{os.getenv('DB_PASSWORD', 'password')}@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '3306')}/{os.getenv('DB_NAME', 'flavormade_db')}" # Changed DB_NAME
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Register all blueprints
app.register_blueprint(user_bp, url_prefix='/api/users') # Changed base prefix for user_bp to be more consistent
app.register_blueprint(preference_bp, url_prefix='/api/users/<int:user_id>/preferences')
app.register_blueprint(meal_history_bp, url_prefix='/api/users/<int:user_id>/meal_history')
app.register_blueprint(restaurant_bp, url_prefix='/api/restaurants')
app.register_blueprint(recommendation_bp, url_prefix='/api/recommendations')


with app.app_context():
    db.create_all() # Creates database tables based on models, if they don't exist

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            # If no static file and no index.html, it's likely an API backend, so 404 is fine.
            # Or, you could return a simple API welcome message.
            return "Welcome to FlavorMade API. No frontend index.html found.", 200 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

