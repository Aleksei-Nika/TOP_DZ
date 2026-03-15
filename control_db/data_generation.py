from sqlalchemy import create_engine, Table, Column, Integer, ForeignKey, CheckConstraint, UniqueConstraint, Enum

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session

engine = create_engine('sqlite:///control_db//generation_alchemy.db')

class Base(DeclarativeBase):
    pass

tag_object = Table(
    'tag_object',
    Base.metadata,
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True),
    Column('object_id', Integer, ForeignKey('objects.id'), primary_key=True)
)

tag_additional_names = Table(
    'tag_additional_names',
    Base.metadata,
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True),
    Column('name_id', Integer, ForeignKey('additional_names.id'), primary_key=True)
)

tag_effects = Table(
    'tag_effects',
    Base.metadata,
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True),
    Column('effect_id', Integer, ForeignKey('effects.id'), primary_key=True)
)

class Object(Base):
    __tablename__ = 'objects'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=True)
    plural_name: Mapped[str] = mapped_column(nullable=True)
    gender: Mapped[str] = mapped_column(Enum('мужской', 'женский', 'средний', name='genger'))
    type_id: Mapped[int] = mapped_column(ForeignKey('objects_types.id'))
    type: Mapped['Object_Type'] = relationship(back_populates='objects')
    tags: Mapped[list['Tag']] = relationship(back_populates='objects', secondary=tag_object)
    __table_args__ = (UniqueConstraint('name', 'plural_name', 'type_id', name='unique_name_type'),
                      )

class Object_Type(Base):
    __tablename__ = 'objects_types'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    objects: Mapped[list['Object']] = relationship(back_populates='type')
    class_object_id: Mapped[int] = mapped_column(ForeignKey('class_objects.id'))
    class_object: Mapped['Class_Object'] = relationship(back_populates='objects_type')

class Objects_Additional_Name(Base):
    __tablename__ = 'additional_names'
    id: Mapped[int] = mapped_column(primary_key=True)
    noun: Mapped[str] = mapped_column(unique=True, nullable=True)
    for_him: Mapped[str] = mapped_column(unique=True, nullable=True)
    for_her: Mapped[str] = mapped_column(unique=True, nullable=True)
    for_medium: Mapped[str] = mapped_column(unique=True, nullable=True)
    for_them: Mapped[str] = mapped_column(unique=True, nullable=True)
    tags: Mapped[list['Tag']] = relationship(back_populates='names', secondary=tag_additional_names)

class Class_Object(Base):
    __tablename__ = 'class_objects'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Enum('локация', 'ингредиент', 'продукт', name='class_object'), unique=True)
    objects_type: Mapped[list['Object_Type']] = relationship(back_populates='class_object')

class Tag(Base):
    __tablename__ = 'tags'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[int] = mapped_column(unique=True, nullable=False)
    objects: Mapped[list['Object']] = relationship(back_populates='tags', secondary=tag_object)
    names: Mapped[list['Objects_Additional_Name']] = relationship(back_populates='tags', secondary=tag_additional_names)
    effects: Mapped[list['Effect']] = relationship(back_populates='tags', secondary=tag_effects)

class Effect(Base):
    __tablename__ = 'effects'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    tags: Mapped[list['Tag']] = relationship(back_populates='effects', secondary=tag_effects)

Base.metadata.create_all(engine)

with Session(engine) as session:
    class CreateTags:
        def __init__(self):
            self._tags = {}
    
        def __getitem__(self, key):
            if key not in self._tags:
                self._tags[key] = Tag(name = key)
            return self._tags[key]

    tags = CreateTags()

    class_object_location = Class_Object(name='локация')
    class_object_ingredient = Class_Object(name='ингредиент')
    class_object_product = Class_Object(name='продукт')

    types_object = (
        Object_Type(name='горы'), #0
        Object_Type(name='поселение'), #1
        Object_Type(name='растительность'), #2
        Object_Type(name='воды'), #3
        Object_Type(name='впадины'), #4
        Object_Type(name='укрепления'), #5
        Object_Type(name='производства'), #6
        Object_Type(name='хозяйства'), #7
        Object_Type(name='захоронения'), #8
    
        Object_Type(name='растения'), #9
        Object_Type(name='грибы'), #10
        Object_Type(name='животные'), #11
        Object_Type(name='минералы'), #12
        Object_Type(name='металлы'), #13

        Object_Type(name='жидкость'), #14
        Object_Type(name='густая масса'), #15
        Object_Type(name='твердое'), #16
        Object_Type(name='газ'), #17
        Object_Type(name='порошок'), #18

    )
    for type_object in types_object[0:9]:
        class_object_location.objects_type.append(type_object)

    for type_object in types_object[9:14]:
        class_object_ingredient.objects_type.append(type_object)

    for type_object in types_object[14:]:
        class_object_product.objects_type.append(type_object)

    objects_location = (
        Object(name='гора', plural_name='горы', gender='женский', type=types_object[0]), #0
        Object(name='возвышенность', plural_name='возвышенности', gender='женский', type=types_object[0]), #1
        Object(name='скала', plural_name='скалы', gender='женский', type=types_object[0]), #2
        Object(name='пик', plural_name='пики', gender='мужской', type=types_object[0]), #3
        Object(name='вершина', plural_name='вершины', gender='женский', type=types_object[0]), #4
        Object(name='хребет', plural_name='хребты', gender='мужской', type=types_object[0]), #5
        Object(name='перевал', plural_name='перевалы', gender='мужской', type=types_object[0]), #6
        Object(name='утёс', plural_name='утёсы', gender='мужской', type=types_object[0]), #7
        Object(name='увал', plural_name='увалы', gender='мужской', type=types_object[0]), #8
        Object(name='плато', plural_name='плато', gender='средний', type=types_object[0]), #9

        Object(name='город', plural_name='города', gender='мужской', type=types_object[1]), #10
        Object(name='деревня', plural_name='деревни', gender='женский', type=types_object[1]), #11
        Object(name='село', plural_name='сёла', gender='средний', type=types_object[1]), #12
        Object(name='хутор', plural_name='хутора', gender='мужской', type=types_object[1]), #13

        Object(name='лес', plural_name='леса', gender='мужской', type=types_object[2]), #14
        Object(name='роща', plural_name='рощи', gender='женский', type=types_object[2]), #15
        Object(name='чаща', plural_name='чащи', gender='женский', type=types_object[2]), #16
        Object(name='глушь', plural_name='глуши', gender='женский', type=types_object[2]), #17
        Object(name='бор', plural_name='боры', gender='мужской', type=types_object[2]), #18
        Object(name='лог', plural_name='лог', gender='мужской', type=types_object[2]), #19

        Object(name='река', plural_name='реки', gender='женский', type=types_object[3]), #20
        Object(name='проток', plural_name='протоки', gender='мужской', type=types_object[3]), #21
        Object(name='озеро', plural_name='озера', gender='средний', type=types_object[3]), #22
        Object(name='плёс', plural_name='плёса', gender='средний', type=types_object[3]), #23
        Object(name='болото', plural_name='болота', gender='средний', type=types_object[3]), #24
        Object(name='топь', plural_name='топи', gender='средний', type=types_object[3]), #25
        Object(name='водопад', plural_name='водопады', gender='мужской', type=types_object[3]), #26
        Object(name='залив', plural_name='заливы', gender='мужской', type=types_object[3]), #27
        Object(name='бухта', plural_name='бухты', gender='женский', type=types_object[3]), #28
        Object(name='пролив', plural_name='проливы', gender='мужской', type=types_object[3]), #29

        Object(name='каньон', plural_name='каньоны', gender='мужской', type=types_object[4]), #30
        Object(name='овраг', plural_name='овраги', gender='мужской', type=types_object[4]), #31
        Object(name='ущелье', plural_name='ущелья', gender='средний', type=types_object[4]), #32
        Object(name='впадина', plural_name='впадины', gender='женский', type=types_object[4]), #33
        Object(name='пустыня', plural_name='пустыни', gender='женский', type=types_object[4]), #34

        Object(name='крепость', plural_name='крепости', gender='женский', type=types_object[5]), #35
        Object(name='цитадель', plural_name='цитадели', gender='женский', type=types_object[5]), #36
        Object(name='бастион', plural_name='бастионы', gender='мужской', type=types_object[5]), #37
        Object(name='форт', plural_name='форты', gender='мужской', type=types_object[5]), #38
        Object(name='замок', plural_name='замки', gender='мужской', type=types_object[5]), #39
        Object(name='башня', plural_name='башни', gender='женский', type=types_object[5]), #40
        Object(name='застава', plural_name='заставы', gender='женский', type=types_object[5]), #42
        Object(name='дозор', plural_name='дозоры', gender='мужской', type=types_object[5]), #43
        Object(name='стена', plural_name='стены', gender='женский', type=types_object[5]), #44

        Object(name='шахта', plural_name='шахты', gender='женский', type=types_object[6]), #45
        Object(name='рудник', plural_name='рудники', gender='мужской', type=types_object[6]), #46
        Object(name='карьер', plural_name='карьеры', gender='мужской', type=types_object[6]), #47
        Object(name='лесопилка', plural_name='лесопилки', gender='женский', type=types_object[6]), #48
        Object(name='кузница', plural_name='кузницы', gender='женский', type=types_object[6]), #49
        
        Object(name='ферма', plural_name='фермы', gender='женский', type=types_object[7]), #50
        Object(name='сад', plural_name='сады', gender='мужской', type=types_object[7]), #51
        Object(name='пастбище', plural_name='пастбища', gender='средний', type=types_object[7]), #52
        
        Object(name=None, plural_name='руины', gender='женский', type=types_object[8]), #53
        Object(name='курган', plural_name='курганы', gender='мужской', type=types_object[8]), #54
        Object(name='могильник', plural_name='могильники', gender='мужской', type=types_object[8]), #55
        Object(name='гробница', plural_name='гробницы', gender='женский', type=types_object[8]), #56

        Object(name='цветок', plural_name='цветки', gender='мужской', type=types_object[9]), #57
        Object(name='лист', plural_name='листья', gender='мужской', type=types_object[9]), #58
        Object(name='бутон', plural_name='бутоны', gender='мужской', type=types_object[9]), #59
        Object(name='лепесток', plural_name='лепестки', gender='мужской', type=types_object[9]), #60
        Object(name='стебель', plural_name='стебли', gender='мужской', type=types_object[9]), #61
        Object(name='лоза', plural_name='лозы', gender='женский', type=types_object[9]), #62
        Object(name='гроздь', plural_name='грозди', gender='женский', type=types_object[9]), #62
        Object(name='корень', plural_name='корни', gender='мужской', type=types_object[9]), #63
        Object(name='клубень', plural_name='клубни', gender='мужской', type=types_object[9]), #64
        Object(name='ягода', plural_name='ягоды', gender='женский', type=types_object[9]), #65
        Object(name='плод', plural_name='плоды', gender='мужской', type=types_object[9]), #66
        Object(name='побег', plural_name='побеги', gender='мужской', type=types_object[9]), #67
        Object(name='трава', plural_name='травы', gender='женский', type=types_object[9]), #67

        Object(name='гриб', plural_name='грибы', gender='мужской', type=types_object[10]), #68
        Object(name='шляпка', plural_name='шляпки', gender='женский', type=types_object[10]), #69
        Object(name='мицелий', plural_name='мицелии', gender='мужской', type=types_object[10]), #70
        Object(name='грибок', plural_name='грибки', gender='мужской', type=types_object[10]), #71
        Object(name='губка', plural_name='губки', gender='мужской', type=types_object[10]), #72
        Object(name='плесень', plural_name=None, gender='мужской', type=types_object[10]), #73
        Object(name=None, plural_name='споры', gender='мужской', type=types_object[10]), #74

        Object(name='панцирь', plural_name='панцири', gender='мужской', type=types_object[11]), #75
        Object(name='кровь', plural_name=None, gender='женский', type=types_object[11]), #76
        Object(name='лапа', plural_name='лапы', gender='женский', type=types_object[11]), #77
        Object(name='ухо', plural_name='уши', gender='средний', type=types_object[11]), #78
        Object(name='зуб', plural_name='зубы', gender='мужской', type=types_object[11]), #79
        Object(name='клык', plural_name='клыки', gender='мужской', type=types_object[11]), #80
        Object(name='крыло', plural_name='крылья', gender='средний', type=types_object[11]), #81
        Object(name='чешуя', plural_name=None, gender='женский', type=types_object[11]), #82
        Object(name='ресница', plural_name='ресницы', gender='женский', type=types_object[11]), #83
        Object(name='коготь', plural_name='когти', gender='мужской', type=types_object[11]), #84
        Object(name='шерсть', plural_name=None, gender='женский', type=types_object[11]), #85
        Object(name='пот', plural_name=None, gender='мужской', type=types_object[11]), #86
        Object(name='слюна', plural_name='слюни', gender='женский', type=types_object[11]), #87
        Object(name='хитин', plural_name=None, gender='мужской', type=types_object[11]), #88
        Object(name='хвост', plural_name='хвосты', gender='мужской', type=types_object[11]), #89
        Object(name='рог', plural_name='рога', gender='мужской', type=types_object[11]), #90
        Object(name='слеза', plural_name='слезы', gender='женский', type=types_object[11]), #91

        Object(name='уголь', plural_name='угли', gender='мужской', type=types_object[12]), #92
        Object(name='соль', plural_name='соли', gender='женский', type=types_object[12]), #93
        Object(name='сера', plural_name=None, gender='женский', type=types_object[12]), #94
        Object(name='кварц', plural_name=None, gender='мужской', type=types_object[12]), #95
        Object(name='аметист', plural_name=None, gender='мужской', type=types_object[12]), #96
        Object(name='слюда', plural_name=None, gender='женский', type=types_object[12]), #97
        Object(name='малахит', plural_name=None, gender='мужской', type=types_object[12]), #98
        Object(name='асбест', plural_name=None, gender='мужской', type=types_object[12]), #99
        Object(name='лазурит', plural_name=None, gender='мужской', type=types_object[12]), #100
        Object(name='янтарь', plural_name=None, gender='мужской', type=types_object[12]), #101
        Object(name='пыль', plural_name=None, gender='женский', type=types_object[12]), #102
        Object(name='камень', plural_name='камни', gender='мужской', type=types_object[12]), #103
        Object(name='стекло', plural_name=None, gender='средний', type=types_object[12]), #104
        Object(name='песок', plural_name='пески', gender='мужской', type=types_object[12]), #105
        Object(name='пепел', plural_name=None, gender='мужской', type=types_object[12]), #106

        Object(name='ртуть', plural_name=None, gender='женский', type=types_object[13]), #107
        Object(name='железо', plural_name=None, gender='средний', type=types_object[13]), #108
        Object(name='медь', plural_name=None, gender='женский', type=types_object[13]), #109
        Object(name='свинец', plural_name=None, gender='мужской', type=types_object[13]), #110
        Object(name='золото', plural_name=None, gender='женский', type=types_object[13]), #111
        Object(name='серебро', plural_name=None, gender='средний', type=types_object[13]), #113
        Object(name='олово', plural_name=None, gender='средний', type=types_object[13]), #114

        Object(name='зелье', plural_name=None, gender='средний', type=types_object[14]), #115
        Object(name='микстура', plural_name=None, gender='женский', type=types_object[14]), #116
        Object(name='эликсир', plural_name=None, gender='средний', type=types_object[14]), #116
        Object(name='настойка', plural_name=None, gender='женский', type=types_object[14]), #116
        Object(name='отвар', plural_name=None, gender='средний', type=types_object[14]), #116
        Object(name='сироп', plural_name=None, gender='средний', type=types_object[14]), #116
        Object(name='бальзам', plural_name=None, gender='средний', type=types_object[14]), #116
        Object(name='снадобье', plural_name=None, gender='средний', type=types_object[14]), #116
        Object(name='вода', plural_name=None, gender='женский', type=types_object[14]), #116
        Object(name='эссенция', plural_name=None, gender='женский', type=types_object[14]), #116
        Object(name='дистиллят', plural_name=None, gender='средний', type=types_object[14]), #116
        Object(name='раствор', plural_name=None, gender='средний', type=types_object[14]), #116

        Object(name='мазь', plural_name=None, gender='женский', type=types_object[15]), #116
        Object(name='крем', plural_name=None, gender='средний', type=types_object[15]), #116
        Object(name='паста', plural_name=None, gender='женский', type=types_object[15]), #116
        Object(name='гель', plural_name=None, gender='средний', type=types_object[15]), #116
        Object(name='смола', plural_name=None, gender='женский', type=types_object[15]), #116
        Object(name='вар', plural_name=None, gender='средний', type=types_object[15]), #116
        Object(name='жир', plural_name=None, gender='средний', type=types_object[15]), #116
        Object(name='деготь', plural_name=None, gender='средний', type=types_object[15]), #116
        Object(name='воск', plural_name=None, gender='средний', type=types_object[15]), #116

        Object(name='камень', plural_name=None, gender='средний', type=types_object[16]), #116
        Object(name='кристалл', plural_name=None, gender='средний', type=types_object[16]), #116
        Object(name='самородок', plural_name=None, gender='средний', type=types_object[16]), #116
        Object(name='брикет', plural_name=None, gender='средний', type=types_object[16]), #116
        Object(name='плитка', plural_name=None, gender='женский', type=types_object[16]), #116
        Object(name='фольга', plural_name=None, gender='женский', type=types_object[16]), #116
        Object(name='проволока', plural_name=None, gender='женский', type=types_object[16]), #116
        Object(name='нить', plural_name=None, gender='женский', type=types_object[16]), #116

        Object(name='дым', plural_name=None, gender='средний', type=types_object[17]), #116
        Object(name='пар', plural_name=None, gender='средний', type=types_object[17]), #116
        Object(name='туман', plural_name=None, gender='средний', type=types_object[17]), #116
        Object(name='облако', plural_name=None, gender='средний', type=types_object[17]), #116
        Object(name='аэрозоль', plural_name=None, gender='средний', type=types_object[17]), #116
        Object(name=None, plural_name='миазмы', gender='средний', type=types_object[17]), #116
        Object(name='эфир', plural_name=None, gender='средний', type=types_object[17]), #116

        Object(name='порох', plural_name=None, gender='средний', type=types_object[18]), #116
        Object(name='пудра', plural_name=None, gender='средний', type=types_object[18]), #116
        Object(name='пыль', plural_name=None, gender='средний', type=types_object[18]), #116
        Object(name='зола', plural_name=None, gender='средний', type=types_object[18]), #116
        Object(name='крупа', plural_name=None, gender='средний', type=types_object[18]), #116
    )

    additional_names = (
        Objects_Additional_Name(noun=None, for_him='горячий', for_her='горячая', for_medium='горячее', for_them='горячие', tags=[tags['тепло'], tags['огонь']]),
        Objects_Additional_Name(noun='шума', for_him='шумный', for_her='шумная', for_medium='шумное', for_them='шумные', tags=[tags['звук'], tags['хаос']]),
        Objects_Additional_Name(noun='возвышения', for_him='возвышенный', for_her='возвышенная', for_medium='возвышенное', for_them='возвышенные', tags=[tags['звук'], tags['хаос']]),
        Objects_Additional_Name(noun='плача', for_him='плачущий', for_her='плачущая', for_medium='плачущее', for_them='плачущие', tags=[tags['страх'], tags['горе']]),
        Objects_Additional_Name(noun='скорби', for_him='скорбящий', for_her='скорбящая', for_medium='скорбящее', for_them='скорбящие', tags=[tags['страх'], tags['горе']]),
        Objects_Additional_Name(noun='солнца', for_him='солнечный', for_her='солнечная', for_medium='солнечное', for_them='солнечные', tags=[tags['тепло'], tags['огонь']]),
        Objects_Additional_Name(noun='цветения', for_him='цветущий', for_her='цветущая', for_medium='цветущее', for_them='цветущие', tags=[tags['тепло'], tags['огонь']]),
        Objects_Additional_Name(noun='пения', for_him='поющий', for_her='поющая', for_medium='поющее', for_them='поющие', tags=[tags['тепло'], tags['огонь']]),
        Objects_Additional_Name(noun='танцов', for_him='танцующий', for_her='танцующая', for_medium='танцующее', for_them='танцующие', tags=[tags['тепло'], tags['огонь']]),
        Objects_Additional_Name(noun='празднества', for_him='праздный', for_her='праздная', for_medium='праздное', for_them='праздные', tags=[tags['тепло'], tags['огонь']]),
        Objects_Additional_Name(noun='тишины', for_him='тихий', for_her='тихая', for_medium='тихое', for_them='тихие', tags=[tags['тепло'], tags['огонь']]),
        Objects_Additional_Name(noun='блеска', for_him='блестящий', for_her='блестящая', for_medium='блестящее', for_them='блестящие', tags=[tags['тепло'], tags['огонь']]),
        Objects_Additional_Name(noun='горения', for_him='горящий', for_her='горящая', for_medium='горящее', for_them='горящие', tags=[tags['тепло'], tags['огонь']]),
        Objects_Additional_Name(noun='смелости', for_him='смелый', for_her='смелая', for_medium='смелое', for_them='смелые', tags=[tags['тепло'], tags['огонь']]),
        Objects_Additional_Name(noun='утопленников', for_him='тонущий', for_her='тонущая', for_medium='тонущее', for_them='тонущие', tags=[tags['тепло'], tags['огонь']]),
        Objects_Additional_Name(noun='бегства', for_him='бегущий', for_her='бегущая', for_medium='бегущее', for_them='бегущие', tags=[tags['тепло'], tags['огонь']]),
        Objects_Additional_Name(noun='спокойствия', for_him='спокойный', for_her='спокойная', for_medium='спокойное', for_them='спокойные', tags=[tags['тепло'], tags['огонь']]),
        Objects_Additional_Name(noun=None, for_him='гремучий', for_her='гремучая', for_medium='гремучее', for_them='гремучие', tags=[tags['тепло'], tags['огонь']]),
        Objects_Additional_Name(noun='жара', for_him='жаркий', for_her='жаркая', for_medium='жаркое', for_them='жаркие', tags=[tags['тепло'], tags['огонь']]),
        Objects_Additional_Name(noun='колючек', for_him='колючий', for_her='колючая', for_medium='колючее', for_them='колючие', tags=[tags['тепло'], tags['огонь']]),
        Objects_Additional_Name(noun='невесомисти', for_him='невесомый', for_her='невесомая', for_medium='невесомые', for_them='невесомое', tags=[tags['тепло'], tags['огонь']]),
        Objects_Additional_Name(noun='парения', for_him='парящий', for_her='парящая', for_medium='парящее', for_them='парящие', tags=[tags['тепло'], tags['огонь']]),
        Objects_Additional_Name(noun='небес', for_him='небесный', for_her='небесная', for_medium='небесное', for_them='небесные', tags=[tags['тепло'], tags['огонь']]),
        Objects_Additional_Name(noun=None, for_him='погибающий', for_her='погибающая', for_medium='погибающее', for_them='погибающие'),
        Objects_Additional_Name(noun='плотности', for_him='плотный', for_her='плотная', for_medium='плотное', for_them='плотные'),
        Objects_Additional_Name(noun='железа', for_him='железный', for_her='железная', for_medium='железное', for_them='железные'),
        Objects_Additional_Name(noun='меди', for_him='медный', for_her='медная', for_medium='медное', for_them='медные'),
        Objects_Additional_Name(noun='дерева', for_him='деревянный', for_her='деревянная', for_medium='деревянное', for_them='деревянные'),
        Objects_Additional_Name(noun=None, for_him='сломленный', for_her='сломленная', for_medium='сломленное', for_them='сломленные'),
        Objects_Additional_Name(noun='непроходимости', for_him='непроходимый', for_her='непроходимая', for_medium='непроходимое', for_them='непроходимые'),
        Objects_Additional_Name(noun='воя', for_him='воющий', for_her='воющая', for_medium='воющее', for_them='воющие'),
        Objects_Additional_Name(noun='вони', for_him='вонючий', for_her='вонючая', for_medium='вонючее', for_them='вонючие'),
        Objects_Additional_Name(noun='духа', for_him='душистый', for_her='душистая', for_medium='душистое', for_them='душистые'),
        Objects_Additional_Name(noun='звона', for_him='звонкий', for_her='звонкая', for_medium='звонкое', for_them='звонкие'),
        Objects_Additional_Name(noun='грохота', for_him='грохочущий', for_her='грохочущая', for_medium='грохочущее', for_them='грохочущие'),
        Objects_Additional_Name(noun='хрусталя', for_him='хрустальный', for_her='хрустальная', for_medium='хрустальное', for_them='хрустальные'),
        Objects_Additional_Name(noun='малости', for_him='малый', for_her='малая', for_medium='малое', for_them='малые'),
        Objects_Additional_Name(noun='раскола', for_him='расколотый', for_her='расколотая', for_medium='расколотое', for_them='расколотые'),
        Objects_Additional_Name(noun='сухости', for_him='сухой', for_her='сухая', for_medium='сухое', for_them='сухие'),
        Objects_Additional_Name(noun='красноты', for_him='красный', for_her='красная', for_medium='красное', for_them='красные'),
        Objects_Additional_Name(noun='синевы', for_him='синий', for_her='синяя', for_medium='синее', for_them='синие'),
        Objects_Additional_Name(noun='темноты', for_him='темный', for_her='темная', for_medium='темное', for_them='темные'),
        Objects_Additional_Name(noun='страха', for_him='страшный', for_her='страшная', for_medium='страшное', for_them='страшные'),
        Objects_Additional_Name(noun='древности', for_him='древний', for_her='древняя', for_medium='древнее', for_them='древние'),
        Objects_Additional_Name(noun='святости', for_him='священный', for_her='священная', for_medium='священное', for_them='священные'),
        Objects_Additional_Name(noun='льда', for_him='ледяной', for_her='ледяная', for_medium='ледяное', for_them='ледяные'),
        Objects_Additional_Name(noun='мороза', for_him='морозный', for_her='морозная', for_medium='морозное', for_them='морозные'),
        Objects_Additional_Name(noun='снега', for_him='снежный', for_her='снежная', for_medium='снежное', for_them='снежные'),
        Objects_Additional_Name(noun='ртути', for_him='ртутный', for_her='ртутная', for_medium='ртутное', for_them='ртутные'),
        Objects_Additional_Name(noun='метеора', for_him='метеорный', for_her='метеорная', for_medium='метеорное', for_them='метеорные'),
        Objects_Additional_Name(noun='гриба', for_him='грибной', for_her='грибная', for_medium='грибное', for_them='грибные'),
        Objects_Additional_Name(noun='цвета', for_him='цветной', for_her='цветная', for_medium='цветное', for_them='цветные'),
        Objects_Additional_Name(noun='рыжины', for_him='рыжий', for_her='рыжая', for_medium='рыжее', for_them='рыжие'),
        Objects_Additional_Name(noun='грома', for_him='громовой', for_her='громовая', for_medium='громовое', for_them='громовые'),
        Objects_Additional_Name(noun='зоркости', for_him='зоркий', for_her='зоркая', for_medium='зоркое', for_them='зоркие'),
        Objects_Additional_Name(noun='яркости', for_him='яркий', for_her='яркая', for_medium='яркое', for_them='яркие'),
        Objects_Additional_Name(noun='кризиса', for_him='кризисный', for_her='кризисная', for_medium='кризисное', for_them='кризисные'),
        Objects_Additional_Name(noun='парадокса', for_him='парадоксальный', for_her='парадоксальная', for_medium='парадоксальное', for_them='парадоксальные'),
        Objects_Additional_Name(noun='моря', for_him='морской', for_her='морская', for_medium='морское', for_them='морские'),
        Objects_Additional_Name(noun='дракона', for_him='драконий', for_her='драконья', for_medium='драконье', for_them='драконьи'),
        Objects_Additional_Name(noun='скользкости', for_him='скользкий', for_her='скользкая', for_medium='скользкое', for_them='скользкие'),
        Objects_Additional_Name(noun='перца', for_him='перечный', for_her='перечная', for_medium='перечное', for_them='перечные'),
        Objects_Additional_Name(noun='паранойи', for_him='параноидальный', for_her='параноидальная', for_medium='параноидальное', for_them='параноидальные'),
        Objects_Additional_Name(noun='тоски', for_him='тоскливый', for_her='тоскливая', for_medium='тоскливое', for_them='тоскливые'),
        Objects_Additional_Name(noun='веселья', for_him='веселый', for_her='веселая', for_medium='веселое', for_them='веселые'),
        Objects_Additional_Name(noun='крутизны', for_him='крутой', for_her='крутая', for_medium='крутое', for_them='крутые'),
        Objects_Additional_Name(noun='ярости', for_him='яростный', for_her='яростная', for_medium='яростное', for_them='яростные'),
        Objects_Additional_Name(noun='квантора', for_him='кванторный', for_her='кванторная', for_medium='кванторное', for_them='кванторные'),
        Objects_Additional_Name(noun='монотонности', for_him='монотонный', for_her='монотонная', for_medium='монотонное', for_them='монотонные'),
        Objects_Additional_Name(noun='ускользания', for_him='ускользающий', for_her='ускользающая', for_medium='ускользающее', for_them='ускользающие'),
        Objects_Additional_Name(noun='хохота', for_him='хохочущий', for_her='хохочущая', for_medium='хохочущее', for_them='хохочущие'),
        Objects_Additional_Name(noun='камня', for_him='каменный', for_her='каменная', for_medium='каменное', for_them='каменные'),
        Objects_Additional_Name(noun='стекла', for_him='стеклянный', for_her='стеклянная', for_medium='стеклянное', for_them='стеклянные'),
        Objects_Additional_Name(noun='золота', for_him='золотой', for_her='золотая', for_medium='золотое', for_them='золотые'),
        Objects_Additional_Name(noun='серебра', for_him='серебряный', for_her='серебряная', for_medium='серебряное', for_them='серебряные'),
        Objects_Additional_Name(noun='бумаги', for_him='бумажный', for_her='бумажная', for_medium='бумажное', for_them='бумажные'),
        Objects_Additional_Name(noun='глины', for_him='глиняный', for_her='глиняная', for_medium='глиняное', for_them='глиняные'),
        Objects_Additional_Name(noun='кожи', for_him='кожаный', for_her='кожаная', for_medium='кожаное', for_them='кожаные'),
        Objects_Additional_Name(noun='шерсти', for_him='шерстяной', for_her='шерстяная', for_medium='шерстяное', for_them='шерстяные'),
        Objects_Additional_Name(noun='пуха', for_him='пуховый', for_her='пуховая', for_medium='пуховое', for_them='пуховые'),
        Objects_Additional_Name(noun='меха', for_him='меховой', for_her='меховая', for_medium='меховое', for_them='меховые'),
        Objects_Additional_Name(noun='пушистости', for_him='пушистый', for_her='пушистая', for_medium='пушистое', for_them='пушистые'),
        Objects_Additional_Name(noun='мокроты', for_him='мокрый', for_her='мокрая', for_medium='мокрое', for_them='мокрые'),
        Objects_Additional_Name(noun='влажности', for_him='влажный', for_her='влажная', for_medium='влажное', for_them='влажные'),
        Objects_Additional_Name(noun='сырости', for_him='сырой', for_her='сырая', for_medium='сырое', for_them='сырые'),
        Objects_Additional_Name(noun='варки', for_him='варёный', for_her='варёная', for_medium='варёное', for_them='варёные'),
        Objects_Additional_Name(noun='жарки', for_him='жареный', for_her='жареная', for_medium='жареное', for_them='жареные'),
        Objects_Additional_Name(noun='печения', for_him='печёный', for_her='печёная', for_medium='печёное', for_them='печёные'),
        Objects_Additional_Name(noun='копчения', for_him='копчёный', for_her='копчёная', for_medium='копчёное', for_them='копчёные'),
        Objects_Additional_Name(noun='солёности', for_him='солёный', for_her='солёная', for_medium='солёное', for_them='солёные'),
        Objects_Additional_Name(noun='сладости', for_him='сладкий', for_her='сладкая', for_medium='сладкое', for_them='сладкие'),
        Objects_Additional_Name(noun='горечи', for_him='горький', for_her='горькая', for_medium='горькое', for_them='горькие'),
        Objects_Additional_Name(noun='кислоты', for_him='кислый', for_her='кислая', for_medium='кислое', for_them='кислые'),
        Objects_Additional_Name(noun='остроты', for_him='острый', for_her='острая', for_medium='острое', for_them='острые'),
        Objects_Additional_Name(noun='гладкости', for_him='гладкий', for_her='гладкая', for_medium='гладкое', for_them='гладкие'),
        Objects_Additional_Name(noun='шершавости', for_him='шершавый', for_her='шершавая', for_medium='шершавое', for_them='шершавые'),
        Objects_Additional_Name(noun='тепла', for_him='тёплый', for_her='тёплая', for_medium='тёплое', for_them='тёплые'),
        Objects_Additional_Name(noun='прохлады', for_him='прохладный', for_her='прохладная', for_medium='прохладное', for_them='прохладные'),
        Objects_Additional_Name(noun='холода', for_him='холодный', for_her='холодная', for_medium='холодное', for_them='холодные'),
        Objects_Additional_Name(noun='зноя', for_him='знойный', for_her='знойная', for_medium='знойное', for_them='знойные')
    )

    effects = (
        Effect(name='Покалывание в кончиках пальцев'),
        Effect(name='Тяжесть в веках'),
        Effect(name='Гул в костях'),
        Effect(name='Жжение в груди'),
        Effect(name='Холод под ложечкой'),
        Effect(name='Мурашки по спине'),
        Effect(name='Зуд в старом шраме'),
        Effect(name='Онемение конечностей'),
        Effect(name='Дрожь в коленях'),
        Effect(name='Чувство невесомости'),
        Effect(name='Сведение мышц'),
        Effect(name='Сухость в горле'),
        Effect(name='Прилив сил'),
        Effect(name='Ломота в суставах'),
        Effect(name='Острые колики'),
        Effect(name='Пульсация в висках'),
        Effect(name='Горячий прилив к лицу'),
        Effect(name='Звенящая пустота внутри'),
        Effect(name='Щекотка в носу'),
        Effect(name='Окаменение затылка'),
        Effect(name='Туннельное зрение'),
        Effect(name='Размытость границ'),
        Effect(name='Обострение слуха'),
        Effect(name='Притупление вкуса'),
        Effect(name='Чувство глубины'),
        Effect(name='Искажение пропорций'),
        Effect(name='Двоение в глазах'),
        Effect(name='Восприятие ауры'),
        Effect(name='Потеря чувства времени'),
        Effect(name='Эхо в голове'),
        Effect(name='Цветной слух (синестезия)'),
        Effect(name='Ощущение чужого взгляда'),
        Effect(name='Чувство дежавю'),
        Effect(name='Остановка внутреннего диалога'),
        Effect(name='Нарушение координации'),
        Effect(name='Потеря чувства голода'),
        Effect(name='Неутолимая жажда'),
        Effect(name='Ощущение падения'),
        Effect(name='Чувство вращения'),
        Effect(name='Размытие реальности'),
        Effect(name='Беспричинный смех'),
        Effect(name='Глубокая печаль'),
        Effect(name='Приступ паранойи'),
        Effect(name='Эйфория'),
        Effect(name='Апатия'),
        Effect(name='Вспышка гнева'),
        Effect(name='Трепет'),
        Effect(name='Ностальгия'),
        Effect(name='Чувство вины'),
        Effect(name='Ощущение всемогущества'),
        Effect(name='Страх высоты'),
        Effect(name='Влюбленность'),
        Effect(name='Омерзение'),
        Effect(name='Жажда справедливости'),
        Effect(name='Ненависть к себе'),
        Effect(name='Любопытство'),
        Effect(name='Обреченность'),
        Effect(name='Надежда'),
        Effect(name='Скука'),
        Effect(name='Тревога'),
        Effect(name='Замедление пульса'),
        Effect(name='Учащение дыхания'),
        Effect(name='Потоотделение'),
        Effect(name='Остановка потоотделения'),
        Effect(name='Слезотечение'),
        Effect(name='Расширение зрачков'),
        Effect(name='Сужение зрачков'),
        Effect(name='Бледность кожи'),
        Effect(name='Покраснение кожи'),
        Effect(name='Появление мурашек'),
        Effect(name='Выпадение волос (временное)'),
        Effect(name='Рост ногтей (ускоренный)'),
        Effect(name='Запах тела (изменение)'),
        Effect(name='Изменение голоса (писклявость)'),
        Effect(name='Изменение голоса (грубость)'),
        Effect(name='Зевота'),
        Effect(name='Икота'),
        Effect(name='Чихание'),
        Effect(name='Кашель'),
        Effect(name='Временная слепота'),
        Effect(name='Вспышка забытого воспоминания'),
        Effect(name='Потеря памяти (кратковременная)'),
        Effect(name='Ясность ума'),
        Effect(name='Спутанность сознания'),
        Effect(name='Навязчивая мысль'),
        Effect(name='Галлюцинации (слуховые)'),
        Effect(name='Галлюцинации (зрительные)'),
        Effect(name='Ощущение "второго дыхания"'),
        Effect(name='Логическое мышление (усиление)'),
        Effect(name='Творческое мышление (усиление)'),
        Effect(name='Понимание языка животных'),
        Effect(name='Ощущение "выхода из тела"'),
        Effect(name='Разговор во сне'),
        Effect(name='Осознанное сновидение'),
        Effect(name='Кошмары'),
        Effect(name='Прокрастинация'),
        Effect(name='Одержимость идеей'),
        Effect(name='Фотографическая память'),
        Effect(name='Дислексия (временная)'),
        Effect(name='Молчаливость')
    )

    session.add_all((class_object_location, class_object_ingredient, class_object_product,
                      *types_object, *objects_location, *additional_names))
    session.commit()