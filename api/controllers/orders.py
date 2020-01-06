import sys
from api import app
from flask import request, jsonify, abort
from api.models.farmer import Farmer
from api.models.product import Product
from api.models.order import Order
from api.models.order_detail import OrderDetail

@app.route('/orders')
def get_orders():
    orders = Order.query.all()
    data = [order.format_short() for order in orders]

    return jsonify({
            'success': True,
            'data': data,
            'count': len(data)
        }), 200


@app.route('/orders/<int:order_id>')
def get_order_details(order_id):
    order = Order.query.get(order_id)

    if not order:
        abort(404)

    data = order.format_long()

    return jsonify({
            'success': True,
            'data': data
        }), 200

@app.route('/orders', methods=['POST'])
def add_order():
    farmer_id = request.json.get('farmer_id', None)
    order_date = request.json.get('order_date', None)
    order_details = request.json.get('order_details', None )

    # validate_order(request)

    order = Order(
        farmer_id=farmer_id,
        order_date=order_date)

    for order_detail in order_details:
        product_id = order_detail.get('product_id')
        line_no = order_detail.get('line_no')
        order_qty = order_detail.get('order_qty')
        line_total = order_detail.get('line_total')

        order_detail = OrderDetail(
            product_id=product_id,
            line_no=line_no,
            order_qty = order_qty,
            line_total = line_total)

        order.order_details.append(order_detail)

    
    error = False
    try:
        order_id = order.add()
    except Exception:
        error = True
        print(sys.exc_info())

    if not error:
        return jsonify({
            'success': True,
            'id': order_id,
            'message': 'order successfully created'
        }), 200

    abort(422)


@app.route('/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    farmer_id = request.json.get('farmer_id', None)
    line_no = order_detail.get('line_no')
    order_date = request.json.get('order_date', None)
    order_details = request.json.get('order_details', None )

    # validate_order(request)

    order = Order.query.get(order_id)

    if not order:
        abort(404)

    order.farmer_id=farmer_id,
    order.order_date=order_date

    for order_detail in order.order_details:
        order.order_details.remove(order_detail)

    for order_detail in order_details:
        product_id = order_detail.get('product_id')
        line_no = order_detail.get('line_no')
        order_qty = order_detail.get('order_qty')
        line_total = order_detail.get('line_total')

        order_detail = OrderDetail(
            product_id=product_id,
            line_no=line_no,
            order_qty = order_qty,
            line_total = line_total)

        order.order_details.append(order_detail)

    error = False
    try:
        order_id = order.update()
    except Exception:
        error = True
        print(sys.exc_info())

    if not error:
        return jsonify({
            'success': True,
            'id': order_id,
            'message': 'order successfully updated'
        }), 200

    abort(422)


@app.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):

    order = Order.query.get(order_id)

    if not order:
        abort(404)

    error = False
    try:
        order_id = order.delete()
    except Exception:
        error = True
        print(sys.exc_info())

    if not error:
        return jsonify({
            'success': True,
            'message': 'order successfully deleted'
        }), 200

    abort(422)



