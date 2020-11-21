from sqlalchemy import Column, Integer, String

from db_worker.engine_creator import SqlAlchemyBase, create_session


class Chats(SqlAlchemyBase):
    __tablename__ = 'chats'

    tg_id = Column(Integer, primary_key=True)

    def __init__(self, tg_id):
        self.tg_id = tg_id

    @staticmethod
    def add_new_chat(tg_id):
        session = create_session()
        new_student = Chats(tg_id)
        session.add(new_student)
        session.commit()

    @staticmethod
    def delete_chat(tg_id):
        session = create_session()
        session.delete(session.query(Chats).get(tg_id))
        session.commit()

    @staticmethod
    def get_by_id(tg_id):
        session = create_session()
        return session.query(Chats).get(tg_id)

    @staticmethod
    def get_all():
        session = create_session()
        return session.query(Chats).all()