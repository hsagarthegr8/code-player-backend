from django.db import models
from django.contrib.auth import get_user_model

import os


user = get_user_model()

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def input_file_upload(instance, filename):
    upload_to = f'files/problems/{instance.problem_setter.username}'
    ensure_dir(upload_to)
    filename = f'{instance.pk}.in'

    return os.path.join(upload_to, filename)
    

def output_file_upload(instance, filename):
    upload_to = f'files/problems/{instance.problem_setter.username}'
    ensure_dir(upload_to)
    filename = f'{instance.pk}.out'

    return os.path.join(upload_to, filename)


class Problem(models.Model):
    problem_setter = models.ForeignKey(user, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    problem_statement = models.TextField(max_length=500)
    input_file = models.FileField(upload_to=input_file_upload, null=True, blank=True)
    output_file = models.FileField(upload_to=output_file_upload, null=True, blank=True)


    def __str__(self):
        return self.name




class Submission(models.Model):

    CHOICES = [
        ('AC', 'Accepted'),
        ('WA', 'Wrong Answer'),
        ('RE', 'Runtime Error')
    ]
    submitted_by = models.ForeignKey(user, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    solution = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    result = models.CharField(max_length=2, choices=CHOICES)

    
    def __str__(self):
        return self.submitted_by.username + ' ' + self.timestamp + ' ' + self.result

