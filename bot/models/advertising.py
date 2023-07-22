from bot.db.database import db


class StatusChoices:
    ACTIVE = 'ACT'
    IN_ACTIVE = 'INACT'


class Test(db.Model):
    __tablename__ = 'main_test'

    id = db.Column(db.BigInteger(), primary_key=True)
    user = db.Column(db.ForeignKey('main_user.id', ondelete='CASCADE'))
    image = db.Column(db.String(255), nullable=False)
    file = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(255), default=StatusChoices.ACTIVE)