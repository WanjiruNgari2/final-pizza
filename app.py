from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from models import db, Restaurant, Pizza, RestaurantPizza
from flask_migrate import Migrate



app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)


@app.route('/')
def index():
    return "Welcome to the Pizza Challenge API!"

# ✅ GET /restaurants
@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurants = Restaurant.query.all()
    return jsonify([{
        'id': r.id,
        'name': r.name,
        'address': r.address
    } for r in restaurants])

# ✅ GET /restaurants/<id>
@app.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if not restaurant:
        return jsonify({"error": "Restaurant not found"}), 404
    
    return jsonify({
        'id': restaurant.id,
        'name': restaurant.name,
        'address': restaurant.address,
        'restaurant_pizzas': [
            {
                'id': rp.id,
                'price': rp.price,
                'pizza': {
                    'id': rp.pizza.id,
                    'name': rp.pizza.name,
                    'ingredients': rp.pizza.ingredients
                }
            } for rp in restaurant.restaurant_pizzas
        ]
    })

# ✅ DELETE /restaurants/<id>
@app.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if not restaurant:
        return jsonify({'error': 'Restaurant not found'}), 404
    db.session.delete(restaurant)
    db.session.commit()
    return '', 204

# ✅ GET /pizzas
@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    pizzas = Pizza.query.all()
    return jsonify([{
        'id': pizza.id,
        'name': pizza.name,
        'ingredients': pizza.ingredients
    } for pizza in pizzas])

# ✅ POST /restaurant_pizzas
@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    data = request.get_json()

    try:
        # Validate required fields
        if not all(key in data for key in ['price', 'pizza_id', 'restaurant_id']):
            raise ValueError("Missing required fields")

        price = data['price']
        pizza_id = data['pizza_id']
        restaurant_id = data['restaurant_id']

        # Explicit price validation (even if model also validates)
        if not (1 <= price <= 30):
            raise ValueError("Price must be between 1 and 30")

        # Get associated records
        pizza = Pizza.query.get(pizza_id)
        restaurant = Restaurant.query.get(restaurant_id)
        
        if not pizza:
            raise ValueError("Pizza not found")
        if not restaurant:
            raise ValueError("Restaurant not found")

        new_rp = RestaurantPizza(
            price=price,
            pizza_id=pizza_id,
            restaurant_id=restaurant_id
        )

        db.session.add(new_rp)
        db.session.commit()

        return jsonify({
            'id': new_rp.id,
            'price': new_rp.price,
            'pizza_id': new_rp.pizza_id,
            'restaurant_id': new_rp.restaurant_id,
            'pizza': {
                'id': pizza.id,
                'name': pizza.name,
                'ingredients': pizza.ingredients
            },
            'restaurant': {
                'id': restaurant.id,
                'name': restaurant.name,
                'address': restaurant.address
            }
        }), 201

    except ValueError as e:
        # Specific validation errors
        return jsonify({'errors': ["validation errors"]}), 400
    except Exception as e:
        # Catch-all for other errors
        return jsonify({'errors': ["validation errors"]}), 400    
if __name__ == '__main__':
    app.run(debug=True)
