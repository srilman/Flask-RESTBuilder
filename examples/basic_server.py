from marshmallow import Schema, fields
from flask import Flask, jsonify
from flask_restbuilder import RestApi

app = Flask(__name__)
api = RestApi(app)


# Marshmallow Schemas
@api.schema(name='Pet')
class PetSchema(Schema):
    id = fields.Integer()
    name = fields.String(required=True)


@api.schema(name='Pets')
class PetsSchema(Schema):
    pets = fields.Nested(PetSchema, required=True, many=True)


@api.route('/pets/')
def get_pets():
    """A cute furry animal endpoint.
    ---
    get:
        tags: [pet]
        description: Get a random pet
        responses:
            200:
                description: A pet to be returned
                schema: PetsSchema
    """
    return jsonify({
        'pets': [{
            'id': 0,
            'name': 'Muffin'
        }]
    })


@app.route('/')
def index():
    return 'Hello, world!'


if __name__ == '__main__':
    # spec = api.generate_spec()
    # print(spec.to_yaml())
    app.run()
