import os
from dotenv import load_dotenv


from flask import Flask
from flask import render_template
from flask import url_for
from flask import request

from routes.default import app as bp_default
from models.connection import db
from flask_migrate import Migrate
from models.model import User
from flask_login import LoginManager
from routes.auth import app as bp_auth



app = Flask(__name__)
app.register_blueprint(bp_default)
app.register_blueprint(bp_auth, url_prefix='/auth')

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///prog1.db")
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "mysecret")

db.init_app(app)

migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user_callback(user_id):
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.execute(stmt).scalar_one_or_none()
    return user

if __name__ == "__main__":
    load_dotenv()  # carica le variabili d'ambiente dal file .env
    app.run(debug=True)