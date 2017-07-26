#!/usr/bin/env python3
from flask import Flask
from flask_cors import CORS

from lock_app import views
from lock_app.keys import INITIAL_KEY
from lock_app.password import save_key

PORT = 8765

save_key(INITIAL_KEY)
app = Flask(__name__)
CORS(app)
views.init(app)

app.run(port=PORT)
