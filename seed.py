from app import app
from models import db, Exercise, Workout, WorkoutExercise

with app.app_context():
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()

    e1 = Exercise(name="Bench Press", category="Strength", description="Barbell bench press on flat bench.")
    e2 = Exercise(name="Squat", category="Strength", description="Barbell back squat.")
    e3 = Exercise(name="Running", category="Cardio", description="Outdoor track running or treadmill.")
    e4 = Exercise(name="Pull-Up", category="Strength", description="Bodyweight pull-ups.")

    db.session.add_all([e1, e2, e3, e4])
    db.session.commit()

    w1 = Workout(name="Upper Body Power", date="2024-06-01", notes="Focus on upper body strength.")
    w2 = Workout(name="Leg Day", date="2024-06-02", notes="Heavy squats and leg press.")

    db.session.add_all([w1, w2])
    db.session.commit()

    we1 = WorkoutExercise(workout_id=w1.id, exercise_id=e1.id, sets=4, reps=8, duration=0)
    we2 = WorkoutExercise(workout_id=w1.id, exercise_id=e4.id, sets=3, reps=10, duration=0)
    we3 = WorkoutExercise(workout_id=w2.id, exercise_id=e2.id, sets=5, reps=5, duration=0)
    we4 = WorkoutExercise(workout_id=w2.id, exercise_id=e3.id, sets=3, reps=15, duration=1800)

    db.session.add_all([we1, we2, we3, we4])
    db.session.commit()

    print("Database seeded successfully!")