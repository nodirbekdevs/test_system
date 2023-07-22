from bot.db.database import db


class StatusChoices:
    ACTIVE = 'ACT'
    IN_ACTIVE = 'INACT'
    PROCESS = 'PRC'


class User(db.Model):
    __tablename__ = 'main_user'

    class TypeChoices:
        STUDENT = 'STD'
        INSTRUCTOR = 'INS'
        ADMIN = 'ADN'

    id = db.Column(db.BigInteger(), primary_key=True)
    telegram_id = db.Column(db.BigInteger(), nullable=True)
    name = db.Column(db.String(255), nullable=True)
    username = db.Column(db.String(255), nullable=True)
    number = db.Column(db.String(255), nullable=True)
    lang = db.Column(db.String(255), nullable=True)
    type = db.Column(db.String(255), default=TypeChoices.STUDENT)
    status = db.Column(db.String(255), default=StatusChoices.ACTIVE)
    updated_at = db.Column(db.DateTime(), default=db.func.now(), onupdate=db.func.now())
    created_at = db.Column(db.DateTime(), default=db.func.now())

    @staticmethod
    async def get_user_by_telegram_id(telegram_id):
        return await User.query.where(User.telegram_id == telegram_id).gino.first()
