from api.database import db
from api.models.order_detail import OrderDetail

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    farmer_id = db.Column(db.Integer, db.ForeignKey(f'farmers.id'), nullable=False)
    order_date = db.Column(db.DateTime, nullable=False)
    order_details = db.relationship('OrderDetail', backref='order', lazy=True,  cascade="all, delete-orphan")

    def farmer_name(self):
        return f'{self.farmer.firstname} {self.farmer.lastname}';

    def get_order_total(self):
        order_total = 0.0
        for order_detail in self.order_details:
            order_total += order_detail.line_total

        return order_total

    def format_short(self):
        return {
            'id': self.id,
            'farmer_id': self.farmer_id,
            'farmer_name': self.farmer_name(),
            'order_date': self.order_date,
            'order_total': self.get_order_total()
        }

    def format_long(self):
        return {
            'id': self.id,
            'farmer_id': self.farmer_id,
            'farmer_name': self.farmer_name(),
            'order_date': self.order_date,
            'order_total': self.get_order_total(),
            'order_details': [detail.format_long() for detail in self.order_details]
        }

    def add(self):
        db.session.add(self)
        db.session.commit()

        return self.id

    def update(self):
        db.session.commit()

        return self.id

    def delete(self):
        db.session.delete(self)
        db.session.commit()
