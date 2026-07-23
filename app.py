from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models import db, Exercise, Workout, WorkoutExercise
from schemas import (
    exercise_schema, exercises_schema,
    workout_schema, workouts_schema,
    workout_exercise_schema
)
from marshmallow import ValidationError

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///workout_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)


@app.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    return jsonify(exercises_schema.dump(exercises)), 200


@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return jsonify({"error": "Exercise not found"}), 404
    return jsonify(exercise_schema.dump(exercise)), 200


@app.route('/exercises', methods=['POST'])
def create_exercise():
    json_data = request.get_json()
    if not json_data:
        return jsonify({"error": "No input data provided"}), 400
    
    try:
        data = exercise_schema.load(json_data)
        
        new_exercise = Exercise(
            name=data['name'],
            category=data['category'],
            description=data.get('description')
        )
        db.session.add(new_exercise)
        db.session.commit()
        return jsonify(exercise_schema.dump(new_exercise)), 201
        
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    except ValueError as err:
        return jsonify({"error": str(err)}), 400


@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return jsonify({"error": "Exercise not found"}), 404
    
    db.session.delete(exercise)
    db.session.commit()
    return jsonify({"message": "Exercise deleted successfully"}), 200


@app.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()
    return jsonify(workouts_schema.dump(workouts)), 200


@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    workout = Workout.query.get(id)
    if not workout:
        return jsonify({"error": "Workout not found"}), 404
    return jsonify(workout_schema.dump(workout)), 200


@app.route('/workouts', methods=['POST'])
def create_workout():
    json_data = request.get_json()
    if not json_data:
        return jsonify({"error": "No input data provided"}), 400
    
    try:
        data = workout_schema.load(json_data)
        
        new_workout = Workout(
            title=data['title'],
            date=data['date'],
            notes=data.get('notes')
        )
        db.session.add(new_workout)
        db.session.commit()
        return jsonify(workout_schema.dump(new_workout)), 201
        
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    except ValueError as err:
        return jsonify({"error": str(err)}), 400


@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = Workout.query.get(id)
    if not workout:
        return jsonify({"error": "Workout not found"}), 404
    
    db.session.delete(workout)
    db.session.commit()
    return jsonify({"message": "Workout deleted successfully"}), 200


@app.route('/workout_exercises', methods=['POST'])
def add_exercise_to_workout():
    json_data = request.get_json()
    if not json_data:
        return jsonify({"error": "No input data provided"}), 400
    
    try:
        data = workout_exercise_schema.load(json_data)
        
        workout = Workout.query.get(data['workout_id'])
        exercise = Exercise.query.get(data['exercise_id'])
        
        if not workout:
            return jsonify({"error": "Workout not found"}), 404
        if not exercise:
            return jsonify({"error": "Exercise not found"}), 404

        new_workout_exercise = WorkoutExercise(
            workout_id=data['workout_id'],
            exercise_id=data['exercise_id'],
            sets=data['sets'],
            reps=data['reps'],
            duration=data.get('duration', 0)
        )
        db.session.add(new_workout_exercise)
        db.session.commit()
        return jsonify(workout_exercise_schema.dump(new_workout_exercise)), 201
        
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    except ValueError as err:
        return jsonify({"error": str(err)}), 400


if __name__ == '__main__':
    app.run(port=5555, debug=True)