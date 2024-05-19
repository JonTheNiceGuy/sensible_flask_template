import os

from flask import Flask
from flask_security import Security, SQLAlchemySessionUserDatastore
from app.models import db_session, init_db
from app.models.authentication import User, Role, initial_user_setup

# Create app
app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config['DEBUG'] = True

# Generate a nice key using secrets.token_urlsafe()
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", 'do-not-use-this-weak-key')
# Bcrypt is set as default SECURITY_PASSWORD_HASH, which requires a salt
# Generate a good salt using: secrets.SystemRandom().getrandbits(128)
app.config['SECURITY_PASSWORD_SALT'] = os.environ.get("SECURITY_PASSWORD_SALT", 'do-not-use-this-weak-salt')
# Don't worry if email has findable domain
app.config["SECURITY_EMAIL_VALIDATOR_ARGS"] = {
    "check_deliverability": False if os.environ.get('CHECK_EMAIL_DOMAIN_IS_FINDABLE', 'false').lower == 'false' else True
}
# Enable registration
app.config['SECURITY_REGISTERABLE'] = True if os.environ.get('REGISTRATION_AVAILABLE', 'true').lower() == 'true' else False
app.config['SECURITY_SEND_REGISTER_EMAIL'] = True if os.environ.get('SEND_REGISTRATION_EMAIL', 'false').lower() == 'true' else False

# manage sessions per request - make sure connections are closed and returned
app.teardown_appcontext(lambda exc: db_session.close())

# Setup Flask-Security
user_datastore = SQLAlchemySessionUserDatastore(db_session, User, Role)
app.security = Security(app, user_datastore)

from app.blueprints.welcome import blueprint as welcome_blueprint
app.register_blueprint(welcome_blueprint)

from app.blueprints.user import blueprint as user_blueprint
app.register_blueprint(user_blueprint)

from app.blueprints.admin import blueprint as admin_blueprint
app.register_blueprint(admin_blueprint)

# initial setup
with app.app_context():
    init_db()
    # Create a user and role to test with
    initial_user_setup()

if __name__ == '__main__':
    # run application (can also use flask run)
    app.run()