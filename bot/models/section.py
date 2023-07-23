from bot.db.database import db
from bot.models.user import User
from bot.models.subject import Subject


class StatusChoices:
    ACTIVE = 'ACT'
    IN_ACTIVE = 'INACT'


class Section(db.Model):
    __tablename__ = 'main_section'

    id = db.Column(db.BigInteger(), primary_key=True)
    user_id = db.Column(db.ForeignKey('main_user.id', ondelete='CASCADE'))
    subject_id = db.Column(db.ForeignKey('main_subject.id', ondelete='CASCADE'))
    name = db.Column(db.String(255), nullable=True)
    description = db.Column(db.String(255), nullable=True)
    total_tests = db.Column(db.Integer(), default=0)
    status = db.Column(db.String(255), default=StatusChoices.ACTIVE)
    updated_at = db.Column(db.DateTime(), default=db.func.now(), onupdate=db.func.now())
    created_at = db.Column(db.DateTime(), default=db.func.now())

    @staticmethod
    async def get_by_id(section_id):
        query = Section.outerjoin(User).outerjoin(Subject)

        query = query.where(Section.id == section_id)

        section = await query.gino.load(Section.load(user=User.load, subject=Subject.load)).first()

        return section

    @staticmethod
    async def check_by_name(name):
        return await Subject.query.where(Subject.name == name).gino.first()

    @staticmethod
    async def delete_by_id(section_id):
        return await Section.delete.where(Section.id == section_id).gino.status()