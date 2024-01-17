#!/usr/bin/env python3


from flask import Flask, jsonify, abort, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config.config import Config
from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config.from_object(Config)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../instance/app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  
migrate = Migrate(app, db)



@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    heroes_data = [{"id": hero.id, "name": hero.name, "super_name": hero.super_name} for hero in heroes]
    return jsonify(heroes_data)

@app.route('/heroes/<int:hero_id>', methods=['GET'])
def get_hero(hero_id):
    hero = Hero.query.get(hero_id)
    if hero:
        hero_data = {
            "id": hero.id,
            "name": hero.name,
            "super_name": hero.super_name,
            "powers": [{"id": hp.power.id, "name": hp.power.name, "description": hp.power.description} for hp in hero.hero_powers]
        }
        return jsonify(hero_data)
    else:
        abort(404, {"error": "Hero not found"})

@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    powers_data = [{"id": power.id, "name": power.name, "description": power.description} for power in powers]
    return jsonify(powers_data)

@app.route('/powers/<int:power_id>', methods=['GET', 'PATCH'])
def get_or_update_power(power_id):
    power = Power.query.get(power_id)
    if power:
        if request.method == 'GET':
            power_data = {"id": power.id, "name": power.name, "description": power.description}
            return jsonify(power_data)
        elif request.method == 'PATCH':
            data = request.json
            if 'description' in data:
                power.description = data['description']
                db.session.commit()
                return jsonify({"id": power.id, "name": power.name, "description": power.description})
            else:
                abort(400, {"error": "No valid data provided for update"})
    else:
        abort(404, {"error": "Power not found"})

@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.json
    hero_id = data.get('hero_id')
    power_id = data.get('power_id')
    strength = data.get('strength')

    hero = Hero.query.get(hero_id)
    power = Power.query.get(power_id)

    if hero and power:
        hero_power = HeroPower(hero=hero, power=power, strength=strength)
        db.session.add(hero_power)
        db.session.commit()

        hero_data = {
            "id": hero.id,
            "name": hero.name,
            "super_name": hero.super_name,
            "powers": [{"id": hp.power.id, "name": hp.power.name, "description": hp.power.description} for hp in hero.hero_powers]
        }

        return jsonify(hero_data)
    else:
        abort(400, {"error": "Invalid hero_id or power_id"})

def create_app():
    return app

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, port=5555)
