#!/usr/bin/env python3
from flask import Flask

from lock_app import views
from lock_app.keys import INITIAL_KEY
from lock_app.password import save_key

save_key(INITIAL_KEY)
app = Flask(__name__)
views.init(app)
app.run(debug=True)
