from django.contrib import admin
from .models import User, Subject, Section, Test


admin.site.register(User)
admin.site.register(Subject)
admin.site.register(Section)
admin.site.register(Test)

# Register your models here.
