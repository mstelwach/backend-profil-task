import json
import os
import datetime
import re
import sys
from urllib import request
from sqlalchemy import create_engine, Integer, Column, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

BaseModel = declarative_base()


class Person(BaseModel):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True)
    gender = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    phone = Column(String(100), nullable=False)
    cell = Column(String(100), nullable=False)
    nat = Column(String(100), nullable=False)


class Name(BaseModel):
    __tablename__ = 'name'
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('person.id'))
    title = Column(String(100), nullable=False)
    first = Column(String(100), nullable=False)
    last = Column(String(100), nullable=False)


class Location(BaseModel):
    __tablename__ = 'location'
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('person.id'))
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False)
    postcode = Column(Integer)


class Street(BaseModel):
    __tablename__ = 'street'
    id = Column(Integer, primary_key=True)
    location_id = Column(Integer, ForeignKey('location.id'))
    number = Column(Integer)
    name = Column(String(100), nullable=False)


class Coordinate(BaseModel):
    __tablename__ = 'coordinate'
    id = Column(Integer, primary_key=True)
    location_id = Column(Integer, ForeignKey('location.id'))
    latitude = Column(String(100), nullable=False)
    longitude = Column(String(100), nullable=False)


class Timezone(BaseModel):
    __tablename__ = 'timezone'
    id = Column(Integer, primary_key=True)
    location_id = Column(Integer, ForeignKey('location.id'))
    offset = Column(String(100), nullable=False)
    description = Column(String(100), nullable=False)


class Login(BaseModel):
    __tablename__ = 'login'
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('person.id'))
    uuid = Column(String(100), nullable=False)
    username = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
    salt = Column(String(100), nullable=False)
    md5 = Column(String(100), nullable=False)
    sha1 = Column(String(100), nullable=False)
    sha256 = Column(String(100), nullable=False)


class ID(BaseModel):
    __tablename__ = 'id'
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('person.id'))
    name = Column(String(100))
    value = Column(String(100))


class Dob(BaseModel):
    __tablename__ = 'dob'
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('person.id'))
    date = Column(DateTime)
    age = Column(Integer)
    next_birthday = Column(Integer)


class Registered(BaseModel):
    __tablename__ = 'registered'
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('person.id'))
    date = Column(DateTime)
    age = Column(Integer)


class Database:

    @staticmethod
    def date_format(date):
        date = date.rstrip('Z').replace('T', ' ')
        date_format = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')
        return date_format

    @staticmethod
    def days_next_birthday(birth):
        today = datetime.date.today()
        birth_year, birth_month, birth_day = birth.year, birth.month, birth.day
        if birth_month == 2 and birth_day == 29:
            birth_day = 28
        if today.month == birth_month and today.day >= birth_day or today.month > birth_month:
            next_birthday_year = today.year + 1
        else:
            next_birthday_year = today.year

        next_birthday = datetime.date(next_birthday_year, birth_month, birth_day)
        delta = next_birthday - today
        return delta.days

    @staticmethod
    def clean_special_char(value):
        return re.sub('[^A-Za-z0-9]+', '', value)

    @staticmethod
    def init_db():
        global session
        db = create_engine('sqlite:///persons.db')
        if os.path.exists('persons.db'):
            os.remove('persons.db')

        BaseModel.metadata.create_all(db)
        session = sessionmaker(bind=db)()

    def insert_to_db(self, file=None):
        self.init_db()

        if file:
            with open(file) as f:
                data = json.load(f)
        else:
            random_user_generator = 'https://randomuser.me/api/?results=1000'
            url = request.urlopen(random_user_generator)
            data = json.loads(url.read().decode())

        for d in data['results']:
            person = Person(gender=d['gender'],
                            email=d['email'],
                            phone=self.clean_special_char(d['phone']),
                            cell=self.clean_special_char(d['cell']),
                            nat=d['nat'])
            session.add(person)
            session.commit()

            session.add(Name(owner_id=person.id,
                             title=d['name']['title'],
                             first=d['name']['first'],
                             last=d['name']['last']))

            person_location = Location(owner_id=person.id,
                                       city=d['location']['city'],
                                       state=d['location']['state'],
                                       country=d['location']['country'],
                                       postcode=d['location']['postcode'])
            session.add(person_location)
            session.commit()

            session.add(Street(location_id=person_location.id,
                               number=d['location']['street']['number'],
                               name=d['location']['street']['name']))

            session.add(Coordinate(location_id=person_location.id,
                                   latitude=d['location']['coordinates']['latitude'],
                                   longitude=d['location']['coordinates']['longitude']))

            session.add(Timezone(location_id=person_location.id,
                                 offset=d['location']['timezone']['offset'],
                                 description=d['location']['timezone']['description']))

            session.add(Login(owner_id=person.id,
                              uuid=d['login']['uuid'],
                              username=d['login']['username'],
                              password=d['login']['password'],
                              salt=d['login']['salt'],
                              md5=d['login']['md5'],
                              sha1=d['login']['sha1'],
                              sha256=d['login']['sha256']))

            session.add(ID(owner_id=person.id,
                           name=d['id']['name'],
                           value=d['id']['value']))

            session.add(Dob(owner_id=person.id,
                            date=self.date_format(d['dob']['date']),
                            age=d['dob']['age'],
                            next_birthday=self.days_next_birthday(self.date_format(d['dob']['date']))))

            session.add(Registered(owner_id=person.id,
                                   date=self.date_format(d['registered']['date']),
                                   age=d['registered']['age']))

            session.commit()
        print('Database updated')


if __name__ == '__main__':
    d = Database()
    method = sys.argv[1].lstrip('-')
    args = sys.argv[2:]
    print(getattr(d, method)(*args))
