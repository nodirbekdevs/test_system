from django.db import models
from django.contrib.postgres.fields import ArrayField

nb = dict(null=True, blank=True)
nnb = dict(null=False, blank=False)


class StatusChoices(models.TextChoices):
    ACTIVE = 'ACT', 'Active'
    IN_ACTIVE = 'INACT', 'Inactive'
    PROCESS = 'PRC', 'Process'


class FeedbackStatusChoices(models.TextChoices):
    ACTIVE = 'ACT', 'Active'
    SEEN = 'SN', 'Seen'
    DONE = 'DN', 'Done'


class CreateTracker(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        abstract = True
        ordering = ('-created_at',)


class CreateUpdateTracker(CreateTracker):
    updated_at = models.DateTimeField(auto_now=True)

    class Meta(CreateTracker.Meta):
        abstract = True


class User(CreateUpdateTracker):
    class TypeChoices(models.TextChoices):
        STUDENT = 'STD', 'Студент'
        TEACHER = 'TCH', 'Преподаватель'
        ADMIN = 'ADN', 'Админ'

    telegram_id = models.PositiveBigIntegerField(**nb)
    name = models.CharField(max_length=255, **nb)
    username = models.CharField(max_length=255, **nb)
    number = models.CharField(max_length=255, **nb)
    lang = models.CharField(max_length=255, **nb)
    type = models.CharField(max_length=255, choices=TypeChoices.choices, default=TypeChoices.STUDENT)
    status = models.CharField(max_length=255, choices=StatusChoices.choices, default=StatusChoices.ACTIVE)


class Subject(CreateUpdateTracker):
    name_uz = models.CharField(max_length=255, **nb)
    name_ru = models.CharField(max_length=255, **nb)
    description = models.CharField(max_length=255, **nb)
    status = models.CharField(max_length=255, choices=StatusChoices.choices, default=StatusChoices.ACTIVE)


class Section(CreateUpdateTracker):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, **nb)
    description = models.CharField(max_length=255, **nb)
    total_tests = models.IntegerField(default=0)
    status = models.CharField(max_length=255, choices=StatusChoices.choices, default=StatusChoices.ACTIVE)


class Test(CreateUpdateTracker):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    question = models.CharField(max_length=255, **nnb)
    variants = ArrayField(models.CharField(max_length=255, **nnb))
    correct_answer = models.CharField(max_length=255, **nnb)
    status = models.CharField(max_length=255, choices=StatusChoices.choices, default=StatusChoices.ACTIVE)
    is_testing = models.BooleanField(default=False)


class Feedback(CreateUpdateTracker):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mark = models.CharField(max_length=255, **nnb)
    reason = models.CharField(max_length=255, **nnb)
    is_read = models.BooleanField(default=False)
    status = models.CharField(max_length=255, choices=FeedbackStatusChoices.choices, default=FeedbackStatusChoices.ACTIVE)


class Advertising(CreateUpdateTracker):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    models.ImageField(upload_to='vacancy_images/', **nnb)
    file = models.CharField(max_length=255, **nnb)
    title = models.CharField(max_length=255, **nnb)
    description = models.CharField(max_length=255, **nnb)
    is_send = models.BooleanField(default=False)
    status = models.CharField(max_length=255, choices=StatusChoices.choices, default=StatusChoices.ACTIVE)