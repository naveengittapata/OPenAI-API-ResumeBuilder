import os
from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager

# Load environment variables from .env file
load_dotenv()

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')

    # App config
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')

    # Database config
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Remember me cookie duration (30 days)
    app.config['REMEMBER_COOKIE_DURATION'] = 2592000

    # Ensure instance folder exists
    os.makedirs(os.path.join(basedir, 'instance'), exist_ok=True)

    # Initialize extensions
    from app.models import db, bcrypt
    db.init_app(app)
    bcrypt.init_app(app)

    # Login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'error'
    login_manager.init_app(app)

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from app.auth import auth
    from app.main import main
    app.register_blueprint(auth)
    app.register_blueprint(main)

    # Create database tables
    with app.app_context():
        db.create_all()

    return app
