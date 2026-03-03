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

class Object(Base):
    __tablename__ = 'objects'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    plural_name: Mapped[str] = mapped_column(unique=True, nullable=False)
    gender: Mapped[str] = mapped_column(Enum('мужской', 'женский', 'средний', name='genger'),nullable=False)
    type_id: Mapped[int] = mapped_column(ForeignKey('objects_types.id'))
    type: Mapped['Object_Type'] = relationship(back_populates='objects')
    tags: Mapped[list['Tag']] = relationship(back_populates='objects', secondary=tag_object)

class Object_Type(Base):
    __tablename__ = 'objects_types'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    objects: Mapped[list['Object']] = relationship(back_populates='type')
    class_object_id: Mapped[int] = mapped_column(ForeignKey('ingridients_objects.id'))
    class_object: Mapped['Class_Object'] = relationship(back_populates='')

class Objects_Additional_Name(Base):
    __tablename__ = 'additional_names'
    id: Mapped[int] = mapped_column(primary_key=True)
    noun: Mapped[str] = mapped_column(unique=True, nullable=False)
    for_him: Mapped[str] = mapped_column(unique=True, nullable=False)
    for_her: Mapped[str] = mapped_column(unique=True, nullable=False)
    for_medium: Mapped[str] = mapped_column(unique=True, nullable=False)
    for_them: Mapped[str] = mapped_column(unique=True, nullable=False)
    tags: Mapped[list[Object]] = relationship(back_populates='names', secondary=tag_additional_names)

class Class_Object(Base):
    __tablename__ = 'ingridients_objects'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Enum('локация', 'ингредиент', 'продукт', name='class_object'), unique=True)
    objects_type: Mapped[list['Object_Type']] = relationship(back_populates='class_object')

class Tag(Base):
    __tablename__ = 'tags'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[int] = mapped_column(unique=True, nullable=False)
    objects: Mapped[list[Object]] = relationship(back_populates='tags', secondary=tag_object)
    names: Mapped[list[Object]] = relationship(back_populates='tags', secondary=tag_additional_names)

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
        Object(name='скала', plural_name='скалы', gender='женский', type=types_object[0]), #8
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

        Object(name='цветок', plura_name='цветки', gender='мужской', type=types_object[9]), #57
        Object(name='лист', plura_name='листья', gender='мужской', type=types_object[9]), #58
        Object(name='бутон', plura_name='бутоны', gender='мужской', type=types_object[9]), #59
        Object(name='лепесток', plura_name='лепестки', gender='мужской', type=types_object[9]), #60
        Object(name='стебель', plura_name='стебли', gender='мужской', type=types_object[9]), #61
        Object(name='лоза', plura_name='лозы', gender='женский', type=types_object[9]), #62
        Object(name='гроздь', plura_name='грозди', gender='женский', type=types_object[9]), #62
        Object(name='корень', plura_name='корни', gender='мужской', type=types_object[9]), #63
        Object(name='клубень', plura_name='клубни', gender='мужской', type=types_object[9]), #64
        Object(name='ягода', plura_name='ягоды', gender='женский', type=types_object[9]), #65
        Object(name='плод', plura_name='плоды', gender='мужской', type=types_object[9]), #66
        Object(name='побег', plura_name='побеги', gender='мужской', type=types_object[9]), #67
        Object(name='трава', plura_name='травы', gender='женский', type=types_object[9]), #67

        Object(name='гриб', plura_name='грибы', gender='мужской', type=types_object[10]), #68
        Object(name='шляпка', plura_name='шляпки', gender='женский', type=types_object[10]), #69
        Object(name='мицелий', plura_name='мицелии', gender='мужской', type=types_object[10]), #70
        Object(name='грибок', plura_name='грибки', gender='мужской', type=types_object[10]), #71
        Object(name='губка', plura_name='губки', gender='мужской', type=types_object[10]), #72
        Object(name='плесень', plura_name=None, gender='мужской', type=types_object[10]), #73
        Object(name=None, plura_name='споры', gender='мужской', type=types_object[10]), #74

        Object(name='панцирь', plura_name='панцири', gender='мужской', type=types_object[11]), #75
        Object(name='кровь', plura_name=None, gender='женский', type=types_object[11]), #76
        Object(name='лапа', plura_name='лапы', gender='женский', type=types_object[11]), #77
        Object(name='ухо', plura_name='уши', gender='средний', type=types_object[11]), #78
        Object(name='зуб', plura_name='зубы', gender='мужской', type=types_object[11]), #79
        Object(name='клык', plura_name='клыки', gender='мужской', type=types_object[11]), #80
        Object(name='крыло', plura_name='крылья', gender='средний', type=types_object[11]), #81
        Object(name='чешуя', plura_name=None, gender='женский', type=types_object[11]), #82
        Object(name='ресница', plura_name='ресницы', gender='женский', type=types_object[11]), #83
        Object(name='коготь', plura_name='когти', gender='мужской', type=types_object[11]), #84
        Object(name='шерсть', plura_name=None, gender='женский', type=types_object[11]), #85
        Object(name='пот', plura_name=None, gender='мужской', type=types_object[11]), #86
        Object(name='слюна', plura_name='слюни', gender='женский', type=types_object[11]), #87
        Object(name='хитин', plura_name=None, gender='мужской', type=types_object[11]), #88
        Object(name='хвост', plura_name='хвосты', gender='мужской', type=types_object[11]), #89
        Object(name='рог', plura_name='рога', gender='мужской', type=types_object[11]), #90
        Object(name='слеза', plura_name='слезы', gender='женский', type=types_object[11]), #91

        Object(name='уголь', plura_name='угли', gender='мужской', type=types_object[12]), #92
        Object(name='соль', plura_name='соли', gender='женский', type=types_object[12]), #93
        Object(name='сера', plura_name=None, gender='женский', type=types_object[12]), #94
        Object(name='кварц', plura_name=None, gender='мужской', type=types_object[12]), #95
        Object(name='аметист', plura_name=None, gender='мужской', type=types_object[12]), #96
        Object(name='слюда', plura_name=None, gender='женский', type=types_object[12]), #97
        Object(name='малахит', plura_name=None, gender='мужской', type=types_object[12]), #98
        Object(name='асбест', plura_name=None, gender='мужской', type=types_object[12]), #99
        Object(name='лазурит', plura_name=None, gender='мужской', type=types_object[12]), #100
        Object(name='янтарь', plura_name=None, gender='мужской', type=types_object[12]), #101
        Object(name='пыль', plura_name=None, gender='женский', type=types_object[12]), #102
        Object(name='камень', plura_name='камни', gender='мужской', type=types_object[12]), #103
        Object(name='стекло', plura_name=None, gender='средний', type=types_object[12]), #104
        Object(name='песок', plura_name='пески', gender='мужской', type=types_object[12]), #105
        Object(name='пепел', plura_name=None, gender='мужской', type=types_object[12]), #106

        Object(name='ртуть', plura_name=None, gender='женский', type=types_object[13]), #107
        Object(name='железо', plura_name=None, gender='средний', type=types_object[13]), #108
        Object(name='медь', plura_name=None, gender='женский', type=types_object[13]), #109
        Object(name='свинец', plura_name=None, gender='мужской', type=types_object[13]), #110
        Object(name='золото', plura_name=None, gender='женский', type=types_object[13]), #111
        Object(name='серебро', plura_name=None, gender='средний', type=types_object[13]), #113
        Object(name='олово', plura_name=None, gender='средний', type=types_object[13]), #114

        Object(name='зелье', plura_name=None, gender='средний', type=types_object[14]), #115
        Object(name='микстура', plura_name=None, gender='женский', type=types_object[14]), #116
        Object(name='эликсир', plura_name=None, gender='средний', type=types_object[14]), #116
        Object(name='настойка', plura_name=None, gender='женский', type=types_object[14]), #116
        Object(name='отвар', plura_name=None, gender='средний', type=types_object[14]), #116
        Object(name='сироп', plura_name=None, gender='средний', type=types_object[14]), #116
        Object(name='бальзам', plura_name=None, gender='средний', type=types_object[14]), #116
        Object(name='снадобье', plura_name=None, gender='средний', type=types_object[14]), #116
        Object(name='вода', plura_name=None, gender='женский', type=types_object[14]), #116
        Object(name='эссенция', plura_name=None, gender='женский', type=types_object[14]), #116
        Object(name='дистиллят', plura_name=None, gender='средний', type=types_object[14]), #116
        Object(name='раствор', plura_name=None, gender='средний', type=types_object[14]), #116

        Object(name='мазь', plura_name=None, gender='женский', type=types_object[15]), #116
        Object(name='крем', plura_name=None, gender='средний', type=types_object[15]), #116
        Object(name='паста', plura_name=None, gender='женский', type=types_object[15]), #116
        Object(name='гель', plura_name=None, gender='средний', type=types_object[15]), #116
        Object(name='смола', plura_name=None, gender='женский', type=types_object[15]), #116
        Object(name='вар', plura_name=None, gender='средний', type=types_object[15]), #116
        Object(name='жир', plura_name=None, gender='средний', type=types_object[15]), #116
        Object(name='деготь', plura_name=None, gender='средний', type=types_object[15]), #116
        Object(name='воск', plura_name=None, gender='средний', type=types_object[15]), #116

        Object(name='камень', plura_name=None, gender='средний', type=types_object[16]), #116
        Object(name='кристалл', plura_name=None, gender='средний', type=types_object[16]), #116
        Object(name='самородок', plura_name=None, gender='средний', type=types_object[16]), #116
        Object(name='брикет', plura_name=None, gender='средний', type=types_object[16]), #116
        Object(name='плитка', plura_name=None, gender='женский', type=types_object[16]), #116
        Object(name='фольга', plura_name=None, gender='женский', type=types_object[16]), #116
        Object(name='проволока', plura_name=None, gender='женский', type=types_object[16]), #116
        Object(name='нить', plura_name=None, gender='женский', type=types_object[16]), #116

        Object(name='дым', plura_name=None, gender='средний', type=types_object[17]), #116
        Object(name='пар', plura_name=None, gender='средний', type=types_object[17]), #116
        Object(name='туман', plura_name=None, gender='средний', type=types_object[17]), #116
        Object(name='облако', plura_name=None, gender='средний', type=types_object[17]), #116
        Object(name='аэрозоль', plura_name=None, gender='средний', type=types_object[17]), #116
        Object(name=None, plura_name='миазмы', gender='средний', type=types_object[17]), #116
        Object(name='эфир', plura_name=None, gender='средний', type=types_object[17]), #116

        Object(name='порох', plura_name=None, gender='средний', type=types_object[18]), #116
        Object(name='пудра', plura_name=None, gender='средний', type=types_object[18]), #116
        Object(name='пыль', plura_name=None, gender='средний', type=types_object[18]), #116
        Object(name='зола', plura_name=None, gender='средний', type=types_object[18]), #116
        Object(name='крупа', plura_name=None, gender='средний', type=types_object[18]), #116
    )

    additional_names = (
        Objects_Additional_Name(noun=None, for_him='горячий', for_her='горячая', for_medium='горячее', for_them='горячие' tags=[tags['тепло'], tags['огонь']]),
        Objects_Additional_Name(noun='шума', for_him='шумный', for_her='шумная', for_medium='шумное', for_them='шимные' tags=[tags['звук'], tags['хаос']]),
        Objects_Additional_Name(noun='возвышения', for_him='возвышенный', for_her='возвышенная', for_medium='возвышенное', for_them='возвышенные' tags=[tags['звук'], tags['хаос']]),
        Objects_Additional_Name(noun='плача', for_him='плачущий', for_her='плачущая', for_medium='плачущее', for_them='плачущие' tags=[tags['страх'], tags['горе']]),
        Objects_Additional_Name(noun='скорби', for_him='скорбящий', for_her='скорбящая', for_medium='скорбящее', for_them='скорбящие' tags=[tags['страх'], tags['горе']]),
        Objects_Additional_Name(noun='солнца', for_him='солнечный', for_her='солнечная', for_medium='солнечное', for_them='солнечные' tags=[tags['тепло'], tags['огонь']]),
        Objects_Additional_Name(noun='цветения', for_him='цветущий', for_her='цветущая', for_medium='цветущее', for_them='цветущие' tags=[tags['тепло'], tags['огонь']]),
        Objects_Additional_Name(noun='пения', for_him='поющий', for_her='поющая', for_medium='поющее', for_them='поющие' tags=[tags['тепло'], tags['огонь']]),
        Objects_Additional_Name(noun='танцов', for_him='танцующий', for_her='танцующая', for_medium='танцующее', for_them='танцующие' tags=[tags['тепло'], tags['огонь']]),
        Objects_Additional_Name(noun='празднества', for_him='праздный', for_her='праздная', for_medium='праздное', for_them='праздные' tags=[tags['тепло'], tags['огонь']]),
        Objects_Additional_Name(noun='тишины', for_him='тихий', for_her='тихая', for_medium='тихое', for_them='тихие' tags=[tags['тепло'], tags['огонь']]),
        Objects_Additional_Name(noun='блеска', for_him='блестящий', for_her='блестящая', for_medium='блестящее', for_them='блестящие' tags=[tags['тепло'], tags['огонь']]),
        Objects_Additional_Name(noun='горения', for_him='горящий', for_her='горящая', for_medium='горящее', for_them='горящие' tags=[tags['тепло'], tags['огонь']]),
        Objects_Additional_Name(noun='смелости', for_him='смелый', for_her='смелая', for_medium='смелое', for_them='смелые' tags=[tags['тепло'], tags['огонь']]),
        Objects_Additional_Name(noun='утопленников', for_him='тонущий', for_her='тонущая', for_medium='тонущее', for_them='тонущие' tags=[tags['тепло'], tags['огонь']]),
        Objects_Additional_Name(noun='бегства', for_him='бегущий', for_her='бегущая', for_medium='бегущее', for_them='бегущие' tags=[tags['тепло'], tags['огонь']]),
        Objects_Additional_Name(noun='спокойствия', for_him='спокойный', for_her='спокойная', for_medium='спокойное', for_them='спокойные' tags=[tags['тепло'], tags['огонь']]),
        Objects_Additional_Name(noun=None, for_him='гремучий', for_her='гремучая', for_medium='гремучее', for_them='гремучие' tags=[tags['тепло'], tags['огонь']]),
        Objects_Additional_Name(noun='жара', for_him='жаркий', for_her='жаркая', for_medium='жаркое', for_them='жаркие' tags=[tags['тепло'], tags['огонь']]),
        Objects_Additional_Name(noun='колючек', for_him='колючий', for_her='колючая', for_medium='колючее', for_them='колючие' tags=[tags['тепло'], tags['огонь']]),
        Objects_Additional_Name(noun='невесомисти', for_him='невесомый', for_her='невесомая', for_medium='невесомые', for_them='невесомое' tags=[tags['тепло'], tags['огонь']]),
        Objects_Additional_Name(noun='парения', for_him='парящий', for_her='парящая', for_medium='парящее', for_them='парящие' tags=[tags['тепло'], tags['огонь']]),
        Objects_Additional_Name(noun='небес', for_him='небесный', for_her='небесная', for_medium='небесное', for_them='небесные' tags=[tags['тепло'], tags['огонь']]),
        
    )

    


    object = Object()