from flask import Flask, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__,static_path='/static/static', static_url_path='/static/static/') # else it conflicts with the url routing with 3 variables (see https://stackoverflow.com/questions/17135006/url-routing-conflicts-for-static-files-in-flask-dev-server)

database_file = 'foo5.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + database_file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
