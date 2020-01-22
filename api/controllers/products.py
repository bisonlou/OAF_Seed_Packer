import sys
from flask import request, jsonify, abort
from api.models.product import Product
from api.auth import requires_auth

def products_app(app):
    @app.route('/products')
    @requires_auth('get:products')
    def get_products(payload):
        products = Product.query.all()
        data = [product.format_short() for product in products]

        return jsonify({
                'success': True,
                'data': data,
                'count': len(data)
            }), 200


    @app.route('/products/<int:product_id>')
    @requires_auth('get:product')
    def get_product_detail(payload, product_id):
        product = Product.query.get(product_id)

        if not product:
            abort(404)

        return jsonify({
                'success': True,
                'data': product.format_long()
            }), 200


    @app.route('/products', methods=['POST'])
    @requires_auth('post:product')
    def add_product(payload):
        name = request.json.get('name', None)
        description = request.json.get('description', None)
        qty = request.json.get('qty', None )
        units = request.json.get('unitis', None)
        unit_price = request.json.get('unit_price', None)

        # validate_product(request)

        product = Product(
            name=name,
            description=description,
            qty=qty,
            units=units,
            unit_price=unit_price)

        error = False
        try:
            product_id = product.add()
        except Exception:
            error = True
            print(sys.exc_info())

        if not error:
            return jsonify({
                'success': True,
                'id': product_id,
                'message': 'product successfully created'
            }), 200

        abort(422)

    @app.route('/products/<int:product_id>', methods=['PUT'])
    @requires_auth('put:product')
    def update_product(payload, product_id):
        name = request.json.get('name', None)
        description = request.json.get('description', None)
        qty = request.json.get('qty', None )
        units = request.json.get('unitis', None)
        unit_price = request.json.get('unit_price', None)

        # validate_product(request)

        product = Product.query.get(product_id)

        if not product:
            abort(404)

        product.name=name,
        product.description=description,
        product.qty=qty,
        product.units=units,
        product.unit_price=unit_price

        error = False
        try:
            product_id = product.update()
        except Exception:
            error = True
            print(sys.exc_info())

        if not error:
            return jsonify({
                'success': True,
                'id': product_id,
                'message': 'product successfully updated'
            }), 200

        abort(422)

    @app.route('/products/<int:product_id>', methods=['DELETE'])
    @requires_auth('delete:product')
    def delete_product(payload, product_id):

        product = Product.query.get(product_id)

        if not product:
            abort(404)

        error = False
        try:
            product_id = product.delete()
        except Exception:
            error = True
            print(sys.exc_info())

        if not error:
            return jsonify({
                'success': True,
                'message': 'product successfully deleted'
            }), 200

        abort(422)
