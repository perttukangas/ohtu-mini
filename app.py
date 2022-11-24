from flask import Flask

app = Flask(__name__)

from src.utils import db

from src.routes import routes
from src.routes import user
