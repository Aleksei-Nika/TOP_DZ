from sqlalchemy import (create_engine, ForeignKey,
                        select, String, Float, Integer,
                        Date, Table, Column, not_, func)
from sqlalchemy.orm import (Session, DeclarativeBase,
                            Mapped, mapped_column, 
                            relationship)

from sqlalchemy.exc import NoResultFound

from datetime import date as dt

engine = create_engine('sqlite:///sqlalchemy//gym.db')
class Base(DeclarativeBase):
    pass

class Users(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    age: Mapped[int]
    workouts: Mapped[list['Workouts']] = relationship(back_populates='user')

class Workouts(Base):
    __tablename__ = 'workouts'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped['Users'] = relationship(back_populates='workouts')
    date: Mapped[dt]
    workout_detail: Mapped[list['Workout_Details']] = relationship(back_populates='workout')

class Exercises(Base):
    __tablename__ = 'exercises'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    muscle_group: Mapped[str]
    workout_detail: Mapped[list['Workout_Details']] = relationship(back_populates='exercise')

class Workout_Details(Base):
    __tablename__ = 'workout_details'
    id: Mapped[int] = mapped_column(primary_key=True)
    workout_id: Mapped[int] = mapped_column(ForeignKey('workouts.id'))
    workout: Mapped['Workouts'] = relationship(back_populates='workout_detail')
    exercise_id: Mapped[int] = mapped_column(ForeignKey('exercises.id'))
    exercise: Mapped['Exercises'] = relationship(back_populates='workout_detail')
    sets: Mapped[int]
    reps: Mapped[int]


Base.metadata.create_all(engine)

def add_data_in_tabels():
    with Session(engine) as session:
        data_users_and_exercises = (
            Users(name = 'Иванов Иван Иванович', age = 34),
            Users(name = 'Дмитриев Дмитрий Дмитриевич', age = 29),
            Users(name = 'Ватрушева Наталья Леонидовна', age = 25),
            Users(name = 'Снежкова Ольга Николаевна', age = 31),

            Exercises(name = 'жим штанги лёжа', muscle_group = 'грудь'), # 4
            Exercises(name = 'тяга верзнего блока к груди', muscle_group = 'спина'), # 5
            Exercises(name = 'присядание со штангой', muscle_group = 'ноги'), # 6
            Exercises(name = 'армейский жим', muscle_group = 'плечи'), # 7
            Exercises(name = 'становая тяга', muscle_group = 'спина'), # 8
            Exercises(name = 'подъём штанги на бицепс', muscle_group = 'руки'), # 9
            Exercises(name = 'разгибание на трицепс руки', muscle_group = 'руки'), # 10
            Exercises(name = 'румынская тяга', muscle_group = 'ноги') # 11
        )
        session.add_all(data_users_and_exercises)
        data_workouts = (
            Workouts(user = data_users_and_exercises[0], date = dt(2026, 1, 15)), # 0
            Workouts(user = data_users_and_exercises[0], date = dt(2026, 1, 17)), # 1
            Workouts(user = data_users_and_exercises[0], date = dt(2026, 1, 19)), # 2
            
            Workouts(user = data_users_and_exercises[1], date = dt(2026, 1, 15)), # 3
            Workouts(user = data_users_and_exercises[1], date = dt(2026, 1, 17)), # 4
            Workouts(user = data_users_and_exercises[1], date = dt(2026, 1, 19)), # 5

            Workouts(user = data_users_and_exercises[2], date = dt(2026, 1, 16)), # 6
            Workouts(user = data_users_and_exercises[2], date = dt(2026, 1, 18)), # 7
            Workouts(user = data_users_and_exercises[2], date = dt(2026, 1, 20)), # 8

            Workouts(user = data_users_and_exercises[3], date = dt(2026, 1, 16)), # 9
            Workouts(user = data_users_and_exercises[3], date = dt(2026, 1, 18)), # 10
            Workouts(user = data_users_and_exercises[3], date = dt(2026, 1, 20)) # 11
        )
        session.add_all(data_workouts)

        data_workouts_details = (
            Workout_Details(workout = data_workouts[0], exercise = data_users_and_exercises[4], sets = 4, reps = 12),
            Workout_Details(workout = data_workouts[0], exercise = data_users_and_exercises[9], sets = 4, reps = 12),
            Workout_Details(workout = data_workouts[0], exercise = data_users_and_exercises[10], sets = 4, reps = 16),

            Workout_Details(workout = data_workouts[1], exercise = data_users_and_exercises[8], sets = 4, reps = 12),
            Workout_Details(workout = data_workouts[1], exercise = data_users_and_exercises[5], sets = 4, reps = 12),
            Workout_Details(workout = data_workouts[1], exercise = data_users_and_exercises[10], sets = 4, reps = 16),

            Workout_Details(workout = data_workouts[2], exercise = data_users_and_exercises[6], sets = 4, reps = 12),
            Workout_Details(workout = data_workouts[2], exercise = data_users_and_exercises[11], sets = 4, reps = 12),
            Workout_Details(workout = data_workouts[2], exercise = data_users_and_exercises[7], sets = 4, reps = 16),

            Workout_Details(workout = data_workouts[3], exercise = data_users_and_exercises[4], sets = 4, reps = 12),
            Workout_Details(workout = data_workouts[3], exercise = data_users_and_exercises[9], sets = 4, reps = 12),
            Workout_Details(workout = data_workouts[3], exercise = data_users_and_exercises[10], sets = 4, reps = 16),

            Workout_Details(workout = data_workouts[4], exercise = data_users_and_exercises[8], sets = 4, reps = 12),
            Workout_Details(workout = data_workouts[4], exercise = data_users_and_exercises[5], sets = 4, reps = 12),
            Workout_Details(workout = data_workouts[4], exercise = data_users_and_exercises[10], sets = 4, reps = 16),

            Workout_Details(workout = data_workouts[5], exercise = data_users_and_exercises[6], sets = 4, reps = 12),
            Workout_Details(workout = data_workouts[5], exercise = data_users_and_exercises[11], sets = 4, reps = 12),
            Workout_Details(workout = data_workouts[5], exercise = data_users_and_exercises[7], sets = 4, reps = 16),

            Workout_Details(workout = data_workouts[6], exercise = data_users_and_exercises[4], sets = 4, reps = 12),
            Workout_Details(workout = data_workouts[6], exercise = data_users_and_exercises[9], sets = 4, reps = 12),
            Workout_Details(workout = data_workouts[6], exercise = data_users_and_exercises[10], sets = 4, reps = 16),

            Workout_Details(workout = data_workouts[7], exercise = data_users_and_exercises[8], sets = 4, reps = 12),
            Workout_Details(workout = data_workouts[7], exercise = data_users_and_exercises[5], sets = 4, reps = 12),
            Workout_Details(workout = data_workouts[7], exercise = data_users_and_exercises[10], sets = 4, reps = 16),

            Workout_Details(workout = data_workouts[8], exercise = data_users_and_exercises[6], sets = 4, reps = 12),
            Workout_Details(workout = data_workouts[8], exercise = data_users_and_exercises[11], sets = 4, reps = 12),
            Workout_Details(workout = data_workouts[8], exercise = data_users_and_exercises[7], sets = 4, reps = 16),

            Workout_Details(workout = data_workouts[9], exercise = data_users_and_exercises[4], sets = 4, reps = 12),
            Workout_Details(workout = data_workouts[9], exercise = data_users_and_exercises[9], sets = 4, reps = 12),
            Workout_Details(workout = data_workouts[9], exercise = data_users_and_exercises[10], sets = 4, reps = 16),

            Workout_Details(workout = data_workouts[10], exercise = data_users_and_exercises[5], sets = 4, reps = 12),
            Workout_Details(workout = data_workouts[10], exercise = data_users_and_exercises[8], sets = 4, reps = 12),
            Workout_Details(workout = data_workouts[10], exercise = data_users_and_exercises[10], sets = 4, reps = 16),

            Workout_Details(workout = data_workouts[11], exercise = data_users_and_exercises[6], sets = 4, reps = 12),
            Workout_Details(workout = data_workouts[11], exercise = data_users_and_exercises[11], sets = 4, reps = 12),
            Workout_Details(workout = data_workouts[11], exercise = data_users_and_exercises[7], sets = 4, reps = 16)

        )
        session.add_all(data_workouts_details)
        session.commit()

add_data_in_tabels()
