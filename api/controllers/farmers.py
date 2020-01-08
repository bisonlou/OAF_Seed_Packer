import sys
from api import app
from flask import request, jsonify, abort
from api.models.farmer import Farmer
from api.auth import requires_auth


@app.route('/farmers')
@requires_auth('get:farmers')
def get_famers():
    farmers = Farmer.query.all()
    data = [farmer.format_short() for farmer in farmers]

    return jsonify({
            'success': True,
            'data': data,
            'count': len(data)
        }), 200


@app.route('/farmers', methods=['POST'])
@requires_auth('post:farmer')
def add_farmer():
    firstname = request.json.get('firstname', None)
    lastname = request.json.get('lastname', None)
    phone = request.json.get('phone', None )
    email = request.json.get('email', None)
    country = request.json.get('country', None)
    state = request.json.get('state', None)
    village = request.json.get('village', None)

    # validate_farmer(request)

    farmer = Farmer(
        firstname=firstname,
        lastname=lastname,
        phone=phone,
        email=email,
        country=country,
        state=state,
        village=village)

    error = False
    try:
        farmer_id = farmer.add()
    except Exception:
        error = True
        print(sys.exc_info())

    if not error:
        return jsonify({
            'success': True,
            'id': farmer_id,
            'message': 'farmer successfully created'
        }), 200

    abort(422)


@app.route('/farmers/<int:farmer_id>', methods=['PUT'])
@requires_auth('put:farmer')
def update_farmer(farmer_id):
    firstname = request.json.get('firstname', None)
    lastname = request.json.get('lastname', None)
    phone = request.json.get('phone', None )
    email = request.json.get('email', None)
    country = request.json.get('country', None)
    state = request.json.get('state', None)
    village = request.json.get('village', None)

    # validate_farmer(request)

    farmer = Farmer.query.get(farmer_id)

    if not farmer:
        abort(404)

    farmer.firstname=firstname,
    farmer.lastname=lastname,
    farmer.phone=phone,
    farmer.email=email,
    farmer.country=country,
    farmer.state=state,
    farmer.village=village

    error = False
    try:
        farmer_id = farmer.update()
    except Exception:
        error = True
        print(sys.exc_info())

    if not error:
        return jsonify({
            'success': True,
            'id': farmer_id,
            'message': 'farmer successfully updated'
        }), 200

    abort(422)

@app.route('/farmers/<int:farmer_id>', methods=['DELETE'])
@requires_auth('put:farmer')
def delete_farmer(farmer_id):

    farmer = Farmer.query.get(farmer_id)

    if not farmer:
        abort(404)

    error = False
    try:
        farmer_id = farmer.delete()
    except Exception:
        error = True
        print(sys.exc_info())

    if not error:
        return jsonify({
            'success': True,
            'message': 'farmer successfully deleted'
        }), 200

    abort(422)
