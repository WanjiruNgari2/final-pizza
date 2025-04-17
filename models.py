from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class Restaurant(db.Model):
    __tablename__ = 'restaurants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    restaurant_pizzas = db.relationship('RestaurantPizza', backref='restaurant', lazy=True)

    def to_dict(self):
        # Exclude restaurant_pizzas here
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address
        }

class Pizza(db.Model):
    __tablename__ = 'pizzas'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.String(255), nullable=False)
    restaurant_pizzas = db.relationship('RestaurantPizza', backref='pizza', lazy=True)

    def to_dict(self):
        # Exclude restaurant_pizzas here
        return {
            'id': self.id,
            'name': self.name,
            'ingredients': self.ingredients
        }

class RestaurantPizza(db.Model):
    __tablename__ = 'restaurant_pizzas'

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)

    def __init__(self, price, pizza_id, restaurant_id):
        if price < 1 or price > 30:
            raise ValueError("Price must be between 1 and 30")
        self.price = price
        self.pizza_id = pizza_id
        self.restaurant_id = restaurant_id

