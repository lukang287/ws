from flask import Flask
import os

app = Flask(__name__)
app.config.from_pyfile('config/base_config.py')
if 'production' in os.environ:
    app.config.from_pyfile('config/prod_config.py')
else:
    app.config.from_pyfile('config/dev_config.py')
