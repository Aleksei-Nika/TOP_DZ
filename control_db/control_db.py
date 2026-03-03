from sqlalchemy import create_engine, Table, Column, Integer, ForeignKey, CheckConstraint, UniqueConstraint, Enum

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

type_material_equipment = Table(
    'type_material_equipment',
    Base.metadata,
    Column('type_id', Integer, ForeignKey('types_ingredients.id'), primary_key=True),
    Column('equipment_id', Integer, ForeignKey('equipments.id'), primary_key=True)
)

elements_recipe = Table(
    'elements_recipe',
    Base.metadata,
    Column('recipe_id', Integer, ForeignKey('recipes.id'), primary_key=True),
    Column('recipe_step_id', Integer, ForeignKey('recipe_steps.id'), primary_key=True)
)

class Product(Base):
    __tablename__ = 'products'
    id: Mapped[int] = mapped_column(primary_key=True)
    effects: Mapped[list['Effect']] = relationship(back_populates='products', secondary=product_effect)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    recipe_id: Mapped[int] = mapped_column(ForeignKey('recipes.id'))
    recipe: Mapped['Recipe'] = relationship(back_populates='product')
    shape_id: Mapped[int] = mapped_column(ForeignKey('shapes.id'))
    shape: Mapped['Shape'] = relationship(back_populates='product')
    order: Mapped[list['Order_Details']] = relationship(back_populates='products')
    description: Mapped[str]

class Effect(Base):
    __tablename__ = 'list_effects'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    products: Mapped[list['Product']] = relationship(back_populates='effects', secondary=product_effect)

class Recipe(Base):
    __tablename__ = 'recipes'
    id: Mapped[int] = mapped_column(primary_key=True)
    product: Mapped['Product'] = relationship(back_populates='recipe')
    recipe_steps: Mapped[list['Recipe_Step']] = relationship(back_populates='recipe', secondary=elements_recipe)
    general_process_id: Mapped[int] = mapped_column(ForeignKey('processes.id'))
    general_process: Mapped['Process'] = relationship(back_populates='general_processes')
    description: Mapped[str]

class Recipe_Step(Base):
    __tablename__ = 'recipe_steps'
    id: Mapped[int] = mapped_column(primary_key=True)
    recipe: Mapped[list['Recipe']] = relationship(back_populates='recipe_steps', secondary=elements_recipe)
    ingredient_id: Mapped[int] = mapped_column(ForeignKey('ingredients.id'))
    ingredient: Mapped['Ingredient'] = relationship(back_populates='recipe')
    process_id: Mapped[int] = mapped_column(ForeignKey('processes.id'))
    process: Mapped['Process'] = relationship(back_populates='recipe_step')
    description: Mapped[str]
    
class Ingredient(Base):
    __tablename__ = 'ingredients'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    type_id: Mapped[int] = mapped_column(ForeignKey('types_ingredients.id'))
    type: Mapped['Types_Ingredients'] = relationship(back_populates='ingredient')
    rarity_level: Mapped[int] = mapped_column(CheckConstraint('rarity_level > 0 AND rarity_level < 6', name='Check_rarity_level'))
    location_id: Mapped[int] = mapped_column(ForeignKey('locations.id'))
    location: Mapped['Location'] = relationship(back_populates='ingredients')
    recipe: Mapped[list['Recipe_Step']] = relationship(back_populates='ingredient')

class Types_Ingredients(Base):
    __tablename__ = 'types_ingredients'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    ingredient: Mapped[list['Ingredient']] = relationship(back_populates='type_id')
    equipments: Mapped[list['Equipment']] = relationship(back_populates='type_material', secondary=type_material_equipment)

class Location(Base):
    __tablename__ = 'locations'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    ingredients: Mapped[list['Ingredient']] = relationship(back_populates='location')
    residents: Mapped[list['Client']] = relationship(back_populates='location')
    description: Mapped[str]

class Shape(Base):
    __tablename__ = 'shapes'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    products: Mapped[list['Product']] = relationship(back_populates='shape')

class Process(Base):
    __tablename__ = 'processes'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    processes: Mapped[list['Recipe_Step']] = relationship(back_populates='process')
    general_processes: Mapped[list['Recipe']] = relationship(back_populates='general_process')
    equipment_id: Mapped[int] = mapped_column(ForeignKey('equipments.id'))
    equipment: Mapped['Equipment'] = relationship(back_populates='processes')


class Equipment(Base):
    __tablename__ = 'equipments'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    type_material: Mapped[list['Types_Ingredients']] = relationship(back_populates='equipments', secondary=type_material_equipment)
    processes: Mapped[list[Process]] = relationship(back_populates='equipment')
    description: Mapped[str]

class Client(Base):
    __tablename__ = 'clients'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    family: Mapped[str]
    location_id: Mapped[int] = mapped_column(ForeignKey('locations.id'))
    location: Mapped['Location'] = relationship(back_populates='residents')
    status: Mapped[str]
    activity: Mapped[str]
    orders: Mapped[list['Order']] = relationship(back_populates='client')

class Order(Base):
    __tablename__ = 'orders'
    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey('clients.id'))
    client: Mapped['Client'] = relationship(back_populates='orders')
    price: Mapped[float]
    description: Mapped[str]
    status: Mapped[str] = mapped_column(Enum('исполнен', 'отменен', 'выполняется', name='order_status'))
    details: Mapped[list['Order_Details']] = relationship(back_populates='order')
    __table_args__ = (CheckConstraint('price >= 0', name = 'price'),)


class Order_Details(Base):
    __tablename__ = 'orders_details'
    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id'))
    order: Mapped['Order'] = relationship(back_populates='details')
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'))
    product: Mapped['Product'] = relationship(back_populates='order')
    quantity: Mapped[int]
    __table_args__ = (CheckConstraint('quantity > 0', name = 'quantity'),)


Base.metadata.create_all(engine)

