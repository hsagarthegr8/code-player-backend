from django.contrib import admin
from django.contrib.auth.models import Group

from .models import User, Profile, Skill

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Skill)

admin.site.unregister(Group)