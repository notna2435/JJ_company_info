from flask import Flask
from flask import request
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
import sqlite3
import time
import os
import pandas as pd
import numpy as np

engine = create_engine('sqlite://',
                        connect_args={'check_same_thread': False},
                        poolclass=StaticPool)

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'sample-company-contacts.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = 'sample_python'
db = SQLAlchemy(app)

df = pd.read_csv('Manual Company Data - Sheet1.csv')

print(df.columns)

class Manual(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(250), nullable=False, unique=True)
    award = db.Column(db.String(250))
    link = db.Column(db.String(250))
    email = db.Column(db.String(250))
    phone_number = db.Column(db.String(250))
    address = db.Column(db.String(250))

with app.app_context():
    db.create_all()
    for i in range(0, len(df)):
        new_item = Manual(company_name=df['Company'][i], award=df['Award'][i], link='None',
                              email=df['Email'][i], phone_number=df['Phone'][i], address=df['Address'][i])
        db.session.add(new_item)

    db.session.commit()

