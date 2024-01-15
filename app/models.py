from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from flask_migrate import Migrate

db = SQLAlchemy()

class Power(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)

    @validates('description')
    def validate_description(self, key, description):
        if len(description) < 20:
            raise ValueError("Description must be at least 20 characters long.")
        return description

    def __repr__(self):
        return f"<Power(id={self.id}, name={self.name}, description={self.description[:20]}...)>"

class Hero(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    super_name = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<Hero(id={self.id}, name={self.name}, super_name={self.super_name})>"

class HeroPower(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hero_id = db.Column(db.Integer, db.ForeignKey('hero.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('power.id'), nullable=False)
    strength = db.Column(db.String(50), nullable=False)

    hero = db.relationship('Hero', backref=db.backref('hero_powers', cascade='all, delete-orphan'))
    power = db.relationship('Power', backref=db.backref('hero_powers', cascade='all, delete-orphan'))

    @validates('strength')
    def validate_strength(self, key, strength):
        valid_strengths = ["Strong", "Weak", "Average"]
        if strength not in valid_strengths:
            raise ValueError("Strength must be one of: 'Strong', 'Weak', 'Average'")
        return strength

    def __repr__(self):
        return f"<HeroPower(id={self.id}, hero_id={self.hero_id}, power_id={self.power_id}, strength={self.strength})>"
