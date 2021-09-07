import datetime

from django.db import models
from django.db.models import UniqueConstraint
from django.utils import timezone
from django.contrib import admin
from django.contrib.auth.models import User


class QuestionList(models.Model):
    question_list_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def __str__(self):
        return self.question_list_text


class ResultsModel(models.Model):
    uid = models.IntegerField()
    questionlist = models.ForeignKey(QuestionList, on_delete=models.CASCADE)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField(blank=True, null=True)


class ResultChoiceModel(models.Model):
    choice_id = models.IntegerField(default=0)
    question_id = models.IntegerField(default=0)
    result = models.ForeignKey(ResultsModel, on_delete=models.CASCADE)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['question_id', 'result_id'], name='unique_choice')]


class Question(models.Model):

    def __str__(self):
        return self.question_text

    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently',
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    questionlist = models.ForeignKey(QuestionList, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):

    def __str__(self):
        return self.choice_text

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
