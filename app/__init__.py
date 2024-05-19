import os

from flask import Flask, render_template_string
from flask_security import Security, current_user, auth_required, hash_password, \
     SQLAlchemySessionUserDatastore, permissions_accepted
from app.models import db_session, init_db
from app.models.authentication import User, Role

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

# one time setup
with app.app_context():
    init_db()
    # Create a user and role to test with
    app.security.datastore.find_or_create_role(
        name="user", permissions={"user-read", "user-write"}
    )
    app.security.datastore.find_or_create_role(
        name="admin", permissions={"user-read", "user-write", "admin"}
    )
    db_session.commit()
    first_user = db_session.query(User).first()
    if not first_user:
        app.security.datastore.create_user(
            email=os.environ.get('FIRST_ADMIN_USERNAME', 'admin@example.org'),
            password=hash_password(os.environ.get('FIRST_ADMIN_PASSWORD', 'Default-Password-Yes1')),
            roles=["admin"]
        )
        db_session.commit()

if __name__ == '__main__':
    # run application (can also use flask run)
    app.run()