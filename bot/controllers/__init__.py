from bot.models.section import Section
from bot.models.subject import Subject
from bot.models.test import Test
from bot.models.user import User
from bot.controllers.controller import Controller


section_controller = Controller(Section)
subject_controller = Controller(Subject)
test_controller = Controller(Test)
user_controller = Controller(User)