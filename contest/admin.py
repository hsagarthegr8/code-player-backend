from django.contrib import admin

from .models import Problem, Submission, Contest

admin.site.register(Problem)
admin.site.register(Submission)
admin.site.register(Contest)
