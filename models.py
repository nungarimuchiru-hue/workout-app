from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import CheckConstraint

db = SQLAlchemy()

class Exercise(db.Model):
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True,nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=True)

    workout_exercises = db.relationship('WorkoutExercise', back_populates='exercise', cascade='all, delete-orphan')

    @validates('name')
    def validate_name(self, key, name):
        if not name or not name.strip():
            raise ValueError("Oops! The exercise name cannot be empty.")
        if len(name.strip()) < 2:
            raise ValueError("Oops! The exercise name must be at least 2 characters long.")
        return name.strip()  

    @validates('category')
    def validate_category(self, key, category):
        allowed_categories = ['Strength', 'Cardio', 'Flexibility', 'Balance']
        if category not in allowed_categories:
            raise ValueError(f"Oops! The category must be one of the following: {', '.join(allowed_categories)}.")
        return category

class Workout(db.Model):
    __tablename__ = 'workouts'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    date = db.Column(db.String(20), nullable=False)
    notes = db.Column(db.String(255), nullable=True)

    workout_exercises = db.relationship('WorkoutExercise', back_populates='workout', cascade='all, delete-orphan')

    @validates('name')
    def validate_name(self, key, name):
        if not name or not name.strip():
            raise ValueError("Oops! The workout name cannot be empty.")
        return name.strip()

class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    sets = db.Column(db.Integer, nullable=False)
    reps = db.Column(db.Integer, nullable=False)
    duration = db.Column(db.Integer, nullable=True)  # Duration in seconds for cardio exercises

    workout = db.relationship('Workout', back_populates='workout_exercises')
    exercise = db.relationship('Exercise', back_populates='workout_exercises')

    __table_args__ = (
        CheckConstraint('sets > 0', name='check_sets_positive'),
        CheckConstraint('reps > 0', name='check_reps_positive'),
        CheckConstraint('duration >= 0', name='check_duration_non_negative'),
    )

    @validates('sets')
    def validate_sets(self, key, sets):
        if sets <= 0:
            raise ValueError("Oops! The number of sets must be greater than 0.")
        return sets

    @validates('reps')
    def validate_reps(self, key, reps):
        if reps <= 0:
            raise ValueError("Oops! The number of reps must be greater than 0.")
        return reps