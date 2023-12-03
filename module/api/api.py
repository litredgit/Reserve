import json
from flask import Flask, jsonify
from ..database import db

app = Flask(__name__)

@app.route('/appv1/user', method=['GET'])
def get_user(user:str):
    """check if there is 'user'"""
    with db.get_db() as db_get_user:
        names = db_get_user.check(user)
        if user in names.values():
            return True
        else:
            return False
        
        