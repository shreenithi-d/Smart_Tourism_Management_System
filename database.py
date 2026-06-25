from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(150), nullable=False)

    email = db.Column(db.String(150), unique=True, nullable=False)

    password = db.Column(db.String(255), nullable=False)

    role = db.Column(
        db.String(20),
        nullable=False,
        default="traveler"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    bookings = db.relationship(
        "Booking",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )

    favorites = db.relationship(
        "Favorite",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User {self.email}>"


class Destination(db.Model):
    __tablename__ = "destinations"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(200),
        nullable=False
    )

    location = db.Column(
        db.String(200),
        nullable=False
    )

    category = db.Column(
        db.String(100),
        nullable=False
    )

    price = db.Column(
        db.Float,
        nullable=False
    )

    duration = db.Column(
        db.String(100),
        nullable=False
    )

    rating = db.Column(
        db.Float,
        nullable=False,
        default=4.5
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    image_url = db.Column(
        db.Text,
        nullable=False
    )

    bookings = db.relationship(
        "Booking",
        backref="destination",
        lazy=True,
        cascade="all, delete-orphan"
    )

    favorites = db.relationship(
        "Favorite",
        backref="destination",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Destination {self.name}>"


class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    destination_id = db.Column(
        db.Integer,
        db.ForeignKey("destinations.id"),
        nullable=False
    )

    travel_date = db.Column(
        db.String(50),
        nullable=False
    )

    people = db.Column(
        db.Integer,
        nullable=False
    )

    total_price = db.Column(
        db.Float,
        nullable=False
    )

    status = db.Column(
        db.String(50),
        default="Confirmed"
    )

    def __repr__(self):
        return f"<Booking {self.id}>"


class Favorite(db.Model):
    __tablename__ = "favorites"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    destination_id = db.Column(
        db.Integer,
        db.ForeignKey("destinations.id"),
        nullable=False
    )

    __table_args__ = (
        db.UniqueConstraint(
            "user_id",
            "destination_id",
            name="unique_user_favorite"
        ),
    )

    def __repr__(self):
        return f"<Favorite {self.id}>"