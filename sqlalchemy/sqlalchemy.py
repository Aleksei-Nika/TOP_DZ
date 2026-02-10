from sqlalchemy import (create_engine, ForeignKey,
                        select, String, Float, Integer,
                        Date, Table, Column, not_, func)
from sqlalchemy.orm import (Session, DeclarativeBase,
                            Mapped, mapped_column, 
                            relationship)

from sqlalchemy.exc import NoResultFound

from datetime import date as dt

engine = create_engine('sqlite:///gym.db')
class Base(DeclarativeBase):
    pass

class Users(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    age: Mapped[int]

class Workouts(Base):
    __table__ = 'workouts'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped[list['Users']] = relationship(back_populates='workouts')
    date: Mapped[dt]

class Exercises(Base):
    __table__ = 'exercises'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    muscle_group = Mapped[str]

class Workout_Details(Base):
    __table__ = 'workout_details'
    id: Mapped[int] = mapped_column(primary_key=True)
    workout_id: Mapped[int] = mapped_column(ForeignKey('workouts.id'))
    workout: Mapped[list['Workouts']] = relationship(back_populates='workout_details')
    exercise_id: Mapped[int] = mapped_column(ForeignKey('exercises.id'))
    exercese: Mapped[list['Exercises']] = relationship(back_populates='workout_details')
    sets: Mapped[int]
    rep: Mapped[int]

Base.metadata.create_all(engine)

with Session(engine) as session:
    data_users = (
        Users(name = 'Иванов Иван Иванович', age = 34),
        Users(name = )
    )
