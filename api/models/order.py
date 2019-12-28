from api.database import db
from api.models.order_detail import OrderDetail

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    farmer_id = db.Column(db.Integer, db.ForeignKey(f'farmers.id'), nullable=False)
    order_date = db.Column(db.DateTime, nullable=False)
    order_details = db.relationship('OrderDetail', backref='order', lazy=True,  cascade="all, delete-orphan")

    def format_short(self):
        return {
            'id': self.id,
            'farmer_id': self.farmer_id,
            'order_date': self.order_date
        }

    def format_long(self):
        return {
            'id': self.id,
            'farmer_id': self.farmer_id,
            'order_date': self.order_date,
            'order_details': [detail.format_long() for detail in OrderDetail.query.filter(OrderDetail.order_id==self.id)]
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
