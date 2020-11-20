from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///users.db', echo=False)


Base = declarative_base()
class Student(Base):
    __tablename__ = 'students'
    
    id = Column(Integer, primary_key=True)
    group = Column(String)    
    name = Column(String)
    surname = Column(String)
    secondname = Column(String)
    nickname = Column(String)

    def __init__(self, id, name, surname, secondname, nickname, group):
        self.id = id
        self.name = name
        self.surname = surname
        self.secondname = secondname
        self.nickname = nickname
        self.group = group

    def __repr__(self):
        return "<User(surname='%s', secondname='%s', name='%s', nickname='%s', group='%s')>" % (self.surname, self.secondname, self.name, self.nickname, self.group)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def add_new_student(id, surname, name, secondname, nickname, group):
    new_student = Student(id=id, surname=surname, name=name, secondname=secondname, nickname=nickname, group=group)
    session.add(new_student)
    session.commit()
    print(new_student, "ADDED")

def delete_student(id): 
    session.delete(session.query(Student).get(id))
    session.commit()

# add_new_student(id = 1010120, surname="surname", name="name", secondname='secondname', nickname="nickname", group="group")
# delete_student(1010120)