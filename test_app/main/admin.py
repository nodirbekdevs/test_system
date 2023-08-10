from django.contrib import admin
from .models import User, Subject, Section, Test, Advertising, Feedback


admin.site.register(User)
admin.site.register(Subject)
admin.site.register(Section)
admin.site.register(Test)
admin.site.register(Advertising)
admin.site.register(Feedback)

# Register your models here.
