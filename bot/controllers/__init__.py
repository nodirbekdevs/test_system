from bot.models.section import Section
from bot.models.subject import Subject
from bot.models.test import Test
from bot.models.user import User
from bot.models.feedback import Feedback
from bot.models.advertising import Advertising
from bot.controllers.controller import Controller


advertising_controller = Controller(Advertising)
section_controller = Controller(Section)
subject_controller = Controller(Subject)
test_controller = Controller(Test)
feedback_controller = Controller(Feedback)
user_controller = Controller(User)