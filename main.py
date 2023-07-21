# A web based test app to see dynamically built website using a SQL database showcasing cafes based on user based filters
# Made by Paul Ged

# Import statements
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from random import randrange

# Flask setup
app = Flask(__name__)

#Connect to Database - currently the app uses a local database in folder
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Cafe table Configuration for all the filters
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

# Random cafe output from database
def random_cafe():
    all_cafes = len(db.session.query(Cafe).all())
    chosen_cafe = Cafe.query.get(randrange(1, all_cafes))
    return chosen_cafe

# homepage
@app.route('/')
def home():
    random_cafe()
    return render_template('index.html')

# returns JSON object which outputs into HTML
@app.route('/random')
def random():
    random_caf = random_cafe()
    cafe_json = {'cafe':{
        'can_take_calls': random_caf.can_take_calls,
        'coffee_price' : random_caf.coffee_price,
        'has_sockets': random_caf.has_sockets,
        'has_toilet': random_caf.has_toilet,
        'has_wifi': random_caf.has_wifi,
        'id': random_caf.id,
        'img_url': random_caf.img_url,
        'location': random_caf.location,
        'map_url': random_caf.map_url,
        'name': random_caf.name,
        'seats': random_caf.seats
    }}
    return jsonify(cafe_json)

# Run from here
if __name__ == '__main__':
    app.run(debug=True)
