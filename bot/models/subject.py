from bot.db.database import db


class StatusChoices:
    ACTIVE = 'ACT'
    IN_ACTIVE = 'INACT'


class Subject(db.Model):
    __tablename__ = 'main_subject'

    id = db.Column(db.BigInteger(), primary_key=True)
    name_uz = db.Column(db.String(255), nullable=True)
    name_ru = db.Column(db.String(255), nullable=True)
    description_uz = db.Column(db.String(255), nullable=True)
    description_ru = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(255), default=StatusChoices.ACTIVE)
    updated_at = db.Column(db.DateTime(), default=db.func.now(), onupdate=db.func.now())
    created_at = db.Column(db.DateTime(), default=db.func.now())

    @staticmethod
    async def get_all():
        return await Subject.query.where(Subject.status == StatusChoices.ACTIVE).gino.all()

    @staticmethod
    async def check_by_name(name):
        return await Subject.query.where(Subject.name_uz == name or Subject.name_ru == name).gino.first()