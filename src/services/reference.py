from flask import session
from src.utils.db import connect
from ..utils import reference_type

def add_reference(data):
    print(data)