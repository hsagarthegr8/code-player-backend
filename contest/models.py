from django.db import models
from django.contrib.auth import get_user_model

import os


user = get_user_model()


def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def input_file_upload(instance, filename):
    upload_to = f'files/{instance.contest.contest_code}/problems'
    ensure_dir(upload_to)
    filename = f'{instance.problem_code}.in'

    return os.path.join(upload_to, filename)


def output_file_upload(instance, filename):
    upload_to = f'files/{instance.contest.contest_code}/problems'
    ensure_dir(upload_to)
    filename = f'{instance.problem_code}.out'

    return os.path.join(upload_to, filename)


class Contest(models.Model):
    name = models.CharField(max_length=40)
    contest_code = models.CharField(max_length=20, primary_key=True)
    created_by = models.ForeignKey(user, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return self.name


class Problem(models.Model):
    contest = models.ForeignKey(
        Contest, on_delete=models.CASCADE, related_name='problems')
    problem_setter = models.ForeignKey(
        user, on_delete=models.CASCADE, related_name='problems')
    problem_code = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=40)
    problem_statement = models.TextField(max_length=500)
    input_file = models.FileField(
        upload_to=input_file_upload, null=True, blank=True)
    output_file = models.FileField(
        upload_to=output_file_upload, null=True, blank=True)

    def __str__(self):
        return self.problem_code

    @property
    def total_submissions(self):
        return len(self.submissions.all())

    @property
    def successful_submissions(self):
        return len(self.submissions.filter(result='AC'))

    @property
    def accuracy(self):
        if self.total_submissions:
            return self.successful_submissions * 100 / self.total_submissions
        return 0


class Submission(models.Model):

    CHOICES = [
        ('AC', 'Accepted'),
        ('WA', 'Wrong Answer'),
        ('RE', 'Runtime Error')
    ]
    submitted_by = models.ForeignKey(user, on_delete=models.CASCADE)
    problem = models.ForeignKey(
        Problem, on_delete=models.CASCADE, related_name='submissions')
    solution = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    result = models.CharField(max_length=2, choices=CHOICES)

    def __str__(self):
        return self.submitted_by.username + ' ' + self.problem.name + ' ' + self.result
