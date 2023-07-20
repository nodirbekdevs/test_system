from gino.dialects.asyncpg import ARRAY
from bot.db.database import db


class StatusChoices:
    ACTIVE = 'ACT'
    IN_ACTIVE = 'INACT'


class Test(db.Model):
    __tablename__ = 'main_test'

    id = db.Column(db.BigInteger(), primary_key=True)
    user = db.Column(db.ForeignKey('main_user.id', ondelete='CASCADE'))
    subject = db.Column(db.ForeignKey('main_subject.id', ondelete='CASCADE'))
    section = db.Column(db.ForeignKey('main_section.id', ondelete='CASCADE'))
    question = db.Column(db.String(255), nullable=False)
    variants = db.Column(ARRAY(db.String(255)), nullable=False)
    correct_answer = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(255), default=StatusChoices.ACTIVE)
    updated_at = db.Column(db.DateTime(), default=db.func.now(), onupdate=db.func.now())
    created_at = db.Column(db.DateTime(), default=db.func.now())