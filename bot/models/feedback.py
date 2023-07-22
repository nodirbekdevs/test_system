from gino.dialects.asyncpg import ARRAY
from bot.db.database import db


class StatusChoices:
    ACTIVE = 'ACT'
    SEEN = 'SN'
    DONE = 'DN'


class Feedback(db.Model):
    __tablename__ = 'main_feedback'

    id = db.Column(db.BigInteger(), primary_key=True)
    user = db.Column(db.ForeignKey('main_user.id', ondelete='CASCADE'))
    mark = db.Column(db.String(255), nullable=False)
    reason = db.Column(db.String(255), nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(255), default=StatusChoices.ACTIVE)
    updated_at = db.Column(db.DateTime(), default=db.func.now(), onupdate=db.func.now())
    created_at = db.Column(db.DateTime(), default=db.func.now())