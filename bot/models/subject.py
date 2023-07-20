from bot.db.database import db


class StatusChoices:
    ACTIVE = 'ACT'
    IN_ACTIVE = 'INACT'


class Subject(db.Model):
    __tablename__ = 'main_subject'

    id = db.Column(db.BigInteger(), primary_key=True)
    name = db.Column(db.String(255), nullable=True)
    description = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(255), default=StatusChoices.ACTIVE)
    updated_at = db.Column(db.DateTime(), default=db.func.now(), onupdate=db.func.now())
    created_at = db.Column(db.DateTime(), default=db.func.now())