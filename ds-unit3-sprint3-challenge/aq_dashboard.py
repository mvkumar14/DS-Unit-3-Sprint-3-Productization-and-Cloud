"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
# from models import DB, Record
import openaq

# Create app object
APP = Flask(__name__)

# Configure app with a databse to use
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

# Telling the database about the app
DB = SQLAlchemy()
DB.init_app(APP)


def get_raw_results():
    api = openaq.OpenAQ()
    status, body = api.measurements(city='Los Angeles', parameter='pm25')
    return status, body

# "Home" route
@APP.route('/')
def root():
    """Base view."""
    # status, body = get_raw_results()
    # tvtuple = time_value_tuple(body)
    results = Record.query.filter(Record.value>=10).all()
    tvtuple = []
    for result in results:
        tvtuple.append([result.datetime,result.value])
    return render_template('base.html',tvtuple=tvtuple)

def time_value_tuple(body):
    time = []
    value = []
    for result in body['results']:
        time.append(result['date']['utc'])
        value.append(result['value'])
    tvtuple = list(zip(time,value))
    return tvtuple


@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data. """
    DB.drop_all()
    DB.create_all()
    status, body = get_raw_results()
    for index, result in enumerate(body['results']):
        row = Record(id=index, datetime=result['date']['utc'], value=result['value'])
        DB.session.add(row)
    DB.session.commit()
    return 'Data Refreshed!'

# Database model:
class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float,nullable=False)

    def __repr__(self):
        return f'<Value {self.value}>'
