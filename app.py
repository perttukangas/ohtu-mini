from flask import Flask
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")

from src.routes import routes
from src.routes import user
