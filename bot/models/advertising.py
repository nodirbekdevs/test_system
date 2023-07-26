from bot.db.database import db


class StatusChoices:
    ACTIVE = 'ACT'
    IN_ACTIVE = 'INACT'


class Advertising(db.Model):
    __tablename__ = 'main_advertising'

    id = db.Column(db.BigInteger(), primary_key=True)
    user_id = db.Column(db.ForeignKey('main_user.id', ondelete='CASCADE'))
    image = db.Column(db.String(255), nullable=False)
    file = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(255), default=StatusChoices.ACTIVE)
    updated_at = db.Column(db.DateTime(), default=db.func.now(), onupdate=db.func.now())
    created_at = db.Column(db.DateTime(), default=db.func.now())

    @staticmethod
    async def get_pagination(query, offset, limit):
        return await Advertising.query.where(Advertising.status == query['status']).offset(offset).limit(limit).gino.all()

    @staticmethod
    async def get_one(advertising_id):
        return await Advertising.query.where(Advertising.id == advertising_id).gino.first()

    @staticmethod
    async def count(status=None):
        count = await db.select([db.func.count()]).select_from(Advertising).gino.scalar()

        if status:
            count = await db.select([db.func.count()]).where(Advertising.status == status).gino.scalar()

        return count
