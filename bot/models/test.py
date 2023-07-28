from gino.dialects.asyncpg import ARRAY
from bot.db.database import db


class StatusChoices:
    ACTIVE = 'ACT'
    IN_ACTIVE = 'INACT'


class Test(db.Model):
    __tablename__ = 'main_test'

    id = db.Column(db.BigInteger(), primary_key=True)
    user_id = db.Column(db.ForeignKey('main_user.id', ondelete='CASCADE'))
    subject_id = db.Column(db.ForeignKey('main_subject.id', ondelete='CASCADE'))
    section_id = db.Column(db.ForeignKey('main_section.id', ondelete='CASCADE'))
    image = db.Column(db.String(255), nullable=False)
    question_uz = db.Column(db.String(255), nullable=False)
    question_ru = db.Column(db.String(255), nullable=False)
    variants_uz = db.Column(ARRAY(db.String(255)), nullable=False)
    variants_ru = db.Column(ARRAY(db.String(255)), nullable=False)
    correct_answer_uz = db.Column(db.String(255), nullable=False)
    correct_answer_ru = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(255), default=StatusChoices.ACTIVE)
    is_testing = db.Column(db.Boolean, default=False)
    updated_at = db.Column(db.DateTime(), default=db.func.now(), onupdate=db.func.now())
    created_at = db.Column(db.DateTime(), default=db.func.now())

    @staticmethod
    async def test_is_being_resolved(section_id, subject_id=None):
        tests = await Test.query.where(Test.section_id == section_id).gino.all()

        if subject_id:
            tests = await Test.query.where(Test.subject_id == subject_id).gino.all()

        for test in tests:
            if test.is_testing:
                return False

        return True
