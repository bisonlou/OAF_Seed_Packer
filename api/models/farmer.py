from api.database import db


class Farmer(db.Model):
    __tablename__ = "farmers"

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    country = db.Column(db.String, nullable=False)
    state = db.Column(db.String, nullable=False)
    village = db.Column(db.String, nullable=False)
    farmer = db.relationship(
        "Order", backref="farmer", lazy=True, cascade="all, delete-orphan"
    )

    def format_short(self):
        return {
            "id": self.id,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "phone": self.phone,
            "email": self.email,
        }

    def format_long(self):
        return {
            "id": self.id,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "phone": self.phone,
            "email": self.email,
            "country": self.country,
            "state": self.state,
            "village": self.village,
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
