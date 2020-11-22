from sqlalchemy import Column, Integer, String

from db_worker.engine_creator import SqlAlchemyBase, create_session


class Student(SqlAlchemyBase):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True, autoincrement=True)
    group = Column(String(10))
    name = Column(String(20))
    surname = Column(String(20))
    secondname = Column(String(20))
    tg_id = Column(Integer)

    def __init__(self, name, surname, secondname, group):
        self.name = name
        self.surname = surname
        self.secondname = secondname
        self.tg_id = None
        self.group = group

    def __repr__(self):
        return "<User(surname='%s', secondname='%s', name='%s', nickname='%s', group='%s')>" % (
            self.surname, self.secondname, self.name, self.tg_id, self.group)

    @staticmethod
    def add_new_student(surname, name, secondname, group):
        session = create_session()
        new_student = Student(surname=surname, name=name, secondname=secondname, group=group)
        session.add(new_student)
        session.commit()

    @staticmethod
    def delete_student(id):
        session = create_session()
        session.delete(session.query(Student).get(id))
        session.commit()

    @staticmethod
    def get_by_id(id):
        session = create_session()
        return session.query(Student).get(id)

    @staticmethod
    def get_by_tg_id(tg_id):
        session = create_session()
        *res, = filter(lambda x: x.tg_id == tg_id, session.query(Student).all())
        if len(res) == 1:
            return res[0]
        return None

    @staticmethod
    def has_authorized(tg_id):
        return Student.get_by_tg_id(tg_id) is not None

    @staticmethod
    def get_by_fio(surname, name, secondname):
        session = create_session()
        *res, = filter(lambda x: x.name == name and x.surname == surname and x.secondname == secondname,
                       session.query(Student).all())
        if len(res) == 1:
            return res[0]
        return None

    def set_tg_id(self, tg_id):
        session = create_session()
        obj = session.query(Student).get(self.id)
        obj.tg_id = tg_id
        self.tg_id = tg_id
        session.commit()
