from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
import http.client

#Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

#Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#Init db
db = SQLAlchemy(app)
#Init ma
ma = Marshmallow(app)

# Selection Class/Model
class Selection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)

    def __init__(self, name):
        self.name = name

# Selection Schema
class SelectionSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name')

#Init Schema
selection_schema = SelectionSchema()
selections_schema = SelectionSchema(many=True)

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

# #Rugby Request Test
# @app.route('/', methods=['GET'])
# def get_rugby():
#     conn = http.client.HTTPSConnection("https://api.sportradar.com/")
#
#     conn.request("GET", "/rugby-union/trial/v3/en/competitions.xml?api_key=a5y3ft5z9a2ejvcym8zkh3xe")
#
#     res = conn.getresponse()
#     data = res.read()
#
#     print(data.decode("utf-8"))

#Run Server
if __name__ == '__main__':
    app.run(debug=True)
