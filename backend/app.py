from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os, requests, json


#Init app
app = Flask(__name__)
CORS(app)
basedir = os.path.abspath(os.path.dirname(__file__))

def get_comps():
    data = requests.get('https://api.sportradar.com/rugby-union/trial/v3/en/seasons.json?api_key=a5y3ft5z9a2ejvcym8zkh3xe')

    competitions = data.json()
    all_competitions = []


#Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Init db
db = SQLAlchemy(app)
#Init ma
ma = Marshmallow(app)

# Season Model
class Season(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    season_id = db.Column(db.Integer)
    name = db.Column(db.String(200), unique=True)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    year = db.Column(db.String(200))

    def __init__ (self, season_id, name, sart_date, end_date, year):
        self.season_id = season_id
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.year = year

# Season Schema
class SeasonSchema(ma.Schema):
    class Meta:
        fields = ('id', 'season_id', 'name', 'start_date', 'end_date', 'year')

#Init Schema
season_schema = SeasonSchema()
seasons_schema = SeasonSchema(many=True)

# Create a Selection
@app.route('/selection', methods=['POST'])
def add_selection():
    name = request.json['name']

    new_selection = Selection(name)

    db.session.add(new_selection)
    db.session.commit()

    return selection_schema.jsonify(new_selection)

#Get All Selections
@app.route('/selection', methods=['GET'])
def get_selections():
    all_selections = Selection.query.all()
    result = selections_schema.dump(all_selections)
    return jsonify(result.data)

#Get Single Selection
@app.route('/selection/<id>', methods=['GET'])
def get_selection(id):
    selection = Selection.query.get(id)
    return selection_schema.jsonify(selection)

# Create a Selection
@app.route('/selection/<id>', methods=['PUT'])
def update_selection(id):
    selection = Selection.query.get(id)

    name = request.json['name']

    selection.name = name

    db.session.commit()

    return selection_schema.jsonify(selection)

#Delete Selection
@app.route('/selection/<id>', methods=['DELETE'])
def delete_selection(id):
    selection = Selection.query.get(id)

    db.session.delete(selection)
    db.session.commit()

    return selection_schema.jsonify(selection)

#Rugby Request Test
@app.route('/', methods=['GET'])
def get_rugby():

    x = requests.get('https://api.sportradar.com/rugby-union/trial/v3/en/competitions.json?api_key=a5y3ft5z9a2ejvcym8zkh3xe')

    data = x.json()
    allPlayers = data['season_players']

    for i in allPlayers:
        players.append(i)

    return json.dumps(allPlayers)

# { "id": "sr:season:86744", "name": "United Rugby Championship 21/22", "start_date": "2021-09-24", "end_date": "2022-06-25", "year": "21/22", "competition_id": "sr:competition:419" }


#Run Server
if __name__ == '__main__':
    app.run(debug=True)
