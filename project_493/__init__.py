from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config['SECRET_KEY'] = 'bea161e19046d27c00575859500b7dd0'  # Probably should delete this to make it less secure
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcpt = Bcrypt()

# Importing here to avoid circular imports
from project_493 import routes
