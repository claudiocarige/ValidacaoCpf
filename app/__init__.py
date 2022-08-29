from flask import Flask

app = Flask(__name__)

app.config['SECRET_KEY'] = '139e5476d653f363468c6d7bf40d1250'

from app.controllers import default
