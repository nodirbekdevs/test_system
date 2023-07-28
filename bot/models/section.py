from bot.db.database import db


class StatusChoices:
    ACTIVE = 'ACT'
    IN_ACTIVE = 'INACT'


class Section(db.Model):
    __tablename__ = 'main_section'

    id = db.Column(db.BigInteger(), primary_key=True)
    user_id = db.Column(db.ForeignKey('main_user.id', ondelete='CASCADE'))
    subject_id = db.Column(db.ForeignKey('main_subject.id', ondelete='CASCADE'))
    name_uz = db.Column(db.String(255), nullable=True)
    name_ru = db.Column(db.String(255), nullable=True)
    description_uz = db.Column(db.String(255), nullable=True)
    description_ru = db.Column(db.String(255), nullable=True)
    total_tests = db.Column(db.Integer(), default=0)
    status = db.Column(db.String(255), default=StatusChoices.ACTIVE)
    updated_at = db.Column(db.DateTime(), default=db.func.now(), onupdate=db.func.now())
    created_at = db.Column(db.DateTime(), default=db.func.now())
