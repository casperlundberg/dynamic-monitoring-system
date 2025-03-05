import json

from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/pets', methods=['GET'])
def get_pets():
    pets = [
        {"id": 1, "name": "Fido", "type": "Dog"},
        {"id": 2, "name": "Whiskers", "type": "Cat"}
    ]
    return jsonify(pets)


@app.route('/pets', methods=['POST'])
def add_pet():
    new_pet = request.json
    return jsonify(new_pet), 201


@app.route('/pets/<int:pet_id>', methods=['GET'])
def get_pet(pet_id):
    pet = {"id": pet_id, "name": "Fido", "type": "Dog"}
    return jsonify(pet)


@app.route('/pets/<int:pet_id>', methods=['PUT'])
def update_pet(pet_id):
    updated_pet = request.json
    updated_pet["id"] = pet_id
    return jsonify(updated_pet)


@app.route('/pets/<int:pet_id>', methods=['DELETE'])
def delete_pet(pet_id):
    return '', 204


if __name__ == '__main__':
    app.run(debug=True)
