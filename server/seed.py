from app import app, db
from models import Restaurant, Pizza, RestaurantPizza
from faker import Faker

fake = Faker()

# Create sample restaurants
def create_sample_data():
    with app.app_context():
        db.create_all()

        # Create some sample restaurants
        for _ in range(3):
            restaurant = Restaurant(
                name=fake.company(),
                address=fake.address()
            )
            db.session.add(restaurant)

        db.session.commit()

        # Create some sample pizzas
        for _ in range(5):
            pizza = Pizza(
                name=fake.word(),
                ingredients=fake.sentence()
            )
            db.session.add(pizza)

        db.session.commit()

        # Create some restaurant_pizzas
        restaurants = Restaurant.query.all()
        pizzas = Pizza.query.all()
        for restaurant in restaurants:
            for pizza in pizzas:
                price = fake.random_number(digits=2)
                if 1 <= price <= 30:
                    restaurant_pizza = RestaurantPizza(
                        price=price, pizza_id=pizza.id, restaurant_id=restaurant.id)
                    db.session.add(restaurant_pizza)

        db.session.commit()

if __name__ == '__main__':
    create_sample_data()
    print("Sample data created successfully!")
