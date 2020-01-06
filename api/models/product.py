from api.database import db

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String, nullable=False)
    qty = db.Column(db.Float, default=0.0)
    units = db.Column(db.String, default='kg')
    unit_price = db.Column(db.Float, default=0.0)
    product = db.relationship('OrderDetail', backref='product', lazy=True, cascade='all, delete-orphan')


    def format_short(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }

    def format_long(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'qty': self.qty,
            'units': self.units,
            'unit_price': self.unit_price,
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

