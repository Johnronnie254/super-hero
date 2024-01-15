# app/seed.py

from models import db, Power, Hero, HeroPower
from app import create_app



app = create_app()
app.app_context().push()

# Seeding powers
powers = [
    Power(name="super strength", description="gives the wielder super-human strengths"),
    Power(name="flight", description="gives the wielder the ability to fly through the skies at supersonic speed"),
    Power(name="super human senses", description="allows the wielder to use her senses at a super-human level"),
    Power(name="elasticity", description="can stretch the human body to extreme lengths"),
]

# Add the powers to the database within the application context
db.session.add_all(powers)
db.session.commit()

# Seeding heroes
heroes = [
    Hero(name="Kamala Khan", super_name="Ms. Marvel"),
    Hero(name="Doreen Green", super_name="Squirrel Girl"),
    Hero(name="Gwen Stacy", super_name="Spider-Gwen"),
    Hero(name="Janet Van Dyne", super_name="The Wasp"),
    Hero(name="Wanda Maximoff", super_name="Scarlet Witch"),
    Hero(name="Carol Danvers", super_name="Captain Marvel"),
    Hero(name="Jean Grey", super_name="Dark Phoenix"),
    Hero(name="Ororo Munroe", super_name="Storm"),
    Hero(name="Kitty Pryde", super_name="Shadowcat"),
    Hero(name="Elektra Natchios", super_name="Elektra"),
]

# Add the heroes to the database within the application context
db.session.add_all(heroes)
db.session.commit()

# Seeding hero powers
strengths = ["Strong", "Weak", "Average"]

for hero in Hero.query.all():
    for _ in range(2):  # You can adjust the number of powers each hero can have
        # get a random power
        power = Power.query.order_by(db.func.random()).first()

        hero_power = HeroPower(hero_id=hero.id, power_id=power.id, strength=strengths[0])
        db.session.add(hero_power)
     

print("🦸‍♀️ Seeding powers, heroes, and hero powers... Done!")
