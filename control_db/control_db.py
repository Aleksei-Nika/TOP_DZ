from sqlalchemy import create_engine, Table, Column, Integer, ForeignKey, CheckConstraint, UniqueConstraint

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

engine = create_engine('sqlite:///control_db//alchemy.db')

class Base(DeclarativeBase):
    pass

product_effect = Table(
    'product_effects',
    Base.metadata,
    Column('product_id', Integer, ForeignKey('products.id'), primary_key=True),
    Column('effect_id', Integer, ForeignKey('list_effects.id'), primary_key=True)
)

class Product(Base):
    __tablename__ = 'products'
    id: Mapped[int] = mapped_column(primary_key=True)
    effects: Mapped[list['Effect']] = relationship(back_populates='products', secondary=product_effect)
    name: Mapped[str] = mapped_column(unique=True, nullable=True)
    recipe_id: Mapped[int] = mapped_column(ForeignKey('recepts.id'))
    recipe: Mapped[list['Recipte']] = relationship(back_populates='products')
    shape_id: Mapped[int] = mapped_column(ForeignKey('shapes.id'))
    shape: Mapped['Shape'] = relationship(back_populates='products')

class Effect(Base):
    __tablename__ = 'list_effects'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=True)
    products: Mapped[list['Product']] = relationship(back_populates='list_effects', secondary=product_effect)

class Recipte(Base):
    __tablename__ = 'recepts'
    id: Mapped[int] = mapped_column(primary_key=True)
    queue: Mapped[int]
    products: Mapped['Product'] = relationship(back_populates='recepts')
    ingredient_id: Mapped[int] = mapped_column(ForeignKey('ingredients.id'))
    ingredient: Mapped['Ingredient'] = relationship(back_populates='recepts')

    __table_args__ = (UniqueConstraint('id', 'queue', name='queue'),)

    
class Ingredient(Base):
    __tablename__ = 'ingredients'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=True)
    type_id: Mapped[int] = mapped_column(ForeignKey('types_ingredients.id'))
    type: Mapped['Types_Ingredients'] = relationship(back_populates='ingredients')
    rarity_level: Mapped[int] = mapped_column(CheckConstraint('rarity_level > 0 AND rarity_level < 6', name='Check_rarity_level'))
    location_id: Mapped[int] = mapped_column(ForeignKey('locations.id'))
    location: Mapped['Location'] = relationship(back_populates='ingredients')
    recipte: Mapped[list['Recipte']] = relationship(back_populates='ingredients')

class Types_Ingredients(Base):
    __tablename__ = 'types_ingredients'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=True)
    Ingredient: Mapped['Ingredient'] = relationship(back_populates='types_ingredients')

class Location(Base):
    __tablename__ = 'locations'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=True)

class Shape(Base):
    __tablename__ = 'shapes'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=True)
    product: Mapped['Product'] = relationship(back_populates='shapes')

Base.metadata.create_all(engine)

