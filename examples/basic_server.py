from marshmallow import Schema, fields
from flask import Flask
from flask_restbuilder import RestApi

app = Flask(__name__)
api = RestApi(app)


# Marshmallow Schemas
@api.schema(name='Pet')
class PetSchema(Schema):
    id = fields.Int()
    name = fields.String(required=True)


@api.schema(name='Pets')
class PetsSchema(Schema):
    pets = fields.Nested(PetSchema, required=True, many=True)


@app.route('/pets/')
@api.route('/pets/')
def get_pets():
    return [{
        'id': 0,
        'name': 'Muffin'
    }]



