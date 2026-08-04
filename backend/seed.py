"""Seed the menu table with an initial pizza lineup. Idempotent — skips if already seeded."""

from app.database import Base, SessionLocal, engine
from app.models.pizza import Pizza

MENU = [
    {"name": "Margherita", "ingredients": "tomato,mozzarella,basil", "unit_price": 12.00, "image_url": "/images/margherita.jpg", "sold_out": False},
    {"name": "Pepperoni", "ingredients": "tomato,mozzarella,pepperoni", "unit_price": 14.50, "image_url": "/images/pepperoni.jpg", "sold_out": False},
    {"name": "Four Cheese", "ingredients": "mozzarella,gorgonzola,parmesan,fontina", "unit_price": 15.00, "image_url": "/images/four-cheese.jpg", "sold_out": False},
    {"name": "Spicy Diavola", "ingredients": "tomato,mozzarella,spicy salami,chili flakes", "unit_price": 15.50, "image_url": "/images/diavola.jpg", "sold_out": False},
    {"name": "Vegetable Garden", "ingredients": "tomato,mozzarella,zucchini,peppers,onion", "unit_price": 13.50, "image_url": "/images/vegetable-garden.jpg", "sold_out": False},
    {"name": "Prosciutto & Rocket", "ingredients": "tomato,mozzarella,prosciutto,rocket,parmesan", "unit_price": 16.00, "image_url": "/images/prosciutto-rocket.jpg", "sold_out": False},
    {"name": "Truffle Mushroom", "ingredients": "mozzarella,mushroom,truffle oil,thyme", "unit_price": 17.00, "image_url": "/images/truffle-mushroom.jpg", "sold_out": True},
    {"name": "BBQ Chicken", "ingredients": "bbq sauce,mozzarella,chicken,red onion", "unit_price": 15.00, "image_url": "/images/bbq-chicken.jpg", "sold_out": False},
]


def seed() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(Pizza).count() == 0:
            db.add_all([Pizza(**item) for item in MENU])
            db.commit()
            print(f"Seeded {len(MENU)} pizzas")
        else:
            print("Menu already seeded, skipping")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
