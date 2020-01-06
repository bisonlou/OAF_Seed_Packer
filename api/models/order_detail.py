from api.database import db

class OrderDetail(db.Model):
    __tablename__ = 'order_details'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    line_no = db.Column(db.Integer)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    order_qty = db.Column(db.Float, nullable=False)
    line_total = db.Column(db.Float, nullable=False)

    def format_long(self):
        return {
            'id': self.id,
            'line_no': self.line_no,
            'order_id': self.order_id,
            'product_id': self.product_id,
            'product_name': self.product.name,
            'order_qty': self.order_qty,
            'line_total': self.line_total
        }

    def add(self):
        db.session.add(self)
        db.session.commit()

        return self.id

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
