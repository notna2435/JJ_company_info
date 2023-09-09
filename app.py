from flask import Flask
from flask import request
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
import sqlite3
from selenium.webdriver.common.keys import Keys
import os.path
import pandas as pd
import random
import string
import time

engine = create_engine('sqlite://',
                        connect_args={'check_same_thread': False},
                        poolclass=StaticPool)

db = SQLAlchemy()
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'sample-company-contacts.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = 'sample_python'
db = SQLAlchemy(app)
# db_name = 'company-contacts.db'
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# print(BASE_DIR)
# db_path = os.path.join(BASE_DIR, db_name)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///company-contacts.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# # app.config['SQLALCHEMY_ENGINE_OPTIONS'] = 'poolclass=StaticPool'
# db.init_app(app)



class Companies(db.Model):
    __tablename__ = 'companies'
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(250), nullable=False, unique=True)
    award = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250))
    phone_number = db.Column(db.String(250))
    address = db.Column(db.String(250))


class Sample(db.Model):
    # __tablename__ = 'sample'
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(250), nullable=False, unique=True)
    award = db.Column(db.String(250), nullable=False)
    link = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250))
    phone_number = db.Column(db.String(250))
    address = db.Column(db.String(250))


class Manual(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(250), nullable=False, unique=True)
    award = db.Column(db.String(250))
    link = db.Column(db.String(250))
    email = db.Column(db.String(250))
    phone_number = db.Column(db.String(250))
    address = db.Column(db.String(250))


def get_random_string(length):
    return ''.join(random.choice(string.ascii_letters) for i in range(length))

time.sleep(2)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/company_contacts')
def company_contacts():
    try:
        contact_info = Sample.query.all()
        # contact_info = pd.read_sql('select * from sample', engine)
        print('ffsfds', contact_info)
    except Exception as e:
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text
    return render_template('company_contacts.html', contacts=contact_info)

@app.route('/manual_data')
def manual_data():
    try:
        manual_contacts = Manual.query.all()
    except Exception as e:
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text
    return render_template('manual_data.html', manual=manual_contacts)

if __name__ == '__main__':
    app.run(debug=True)
