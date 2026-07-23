from flask_marshmallow import Marshmallow
from marshmallow import fields, validate

ma = Marshmallow()

class ExerciseSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=2, max=100))
    category = fields.String(required=True, validate=validate.Length(min=2, max=50))
    description = fields.String(validate=validate.Length(max=255))

    class Meta:
        fields = ("id", "name", "category", "description")


class WorkoutExerciseSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    workout_id = fields.Integer(required=True)
    exercise_id = fields.Integer(required=True)
    
    sets = fields.Integer(required=True, validate=validate.Range(min=1, max=100))
    reps = fields.Integer(required=True, validate=validate.Range(min=1, max=500))
    duration = fields.Integer(validate=validate.Range(min=0))

    exercise = fields.Nested(ExerciseSchema, dump_only=True)

    class Meta:
        fields = ("id", "workout_id", "exercise_id", "sets", "reps", "duration", "exercise")


class WorkoutSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String(required=True, validate=validate.Length(min=2, max=100))
    date = fields.String(required=True)
    notes = fields.String(validate=validate.Length(max=255))

    workout_exercises = fields.List(fields.Nested(WorkoutExerciseSchema), dump_only=True)

    class Meta:
        fields = ("id", "title", "date", "notes", "workout_exercises")


exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

workout_exercise_schema = WorkoutExerciseSchema()
workout_exercises_schema = WorkoutExerciseSchema(many=True)