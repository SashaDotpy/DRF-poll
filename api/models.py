from django.db import models
from django.contrib.auth.models import User
from rest_framework import exceptions


class Poll(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField(default='Описание отсутствует')
    start_at = models.DateTimeField(default=None, blank=True, null=True)
    finish_at = models.DateTimeField(default=None, blank=True, null=True)


class Question(models.Model):
    text = models.TextField()
    question_types = (
        ('text', 'text_answer_form'),
        ('one', 'one_option_answer_form'),
        ('many', 'many_options_answer_form'),
    )
    type = models.CharField(max_length=30, choices=question_types)
    poll = models.ForeignKey(Poll,
                             on_delete=models.CASCADE,
                             related_name='questions')

    def save(self, *args, **kwargs):
        if self.poll.start_at is not None:
            raise exceptions.PermissionDenied
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.poll.start_at is not None:
            raise exceptions.PermissionDenied
        super().delete(self, *args, **kwargs)


class Option(models.Model):
    text = models.TextField(default='Enter text')
    question = models.ForeignKey(Question,
                                 on_delete=models.CASCADE,
                                 related_name='options')


class Answer(models.Model):
    text_form = models.CharField(max_length=300, blank=True)
    poll = models.ForeignKey(Poll,
                             on_delete=models.CASCADE,
                             related_name='answers')

    question = models.ForeignKey(Question,
                                 on_delete=models.CASCADE,
                                 related_name='answers')

    user = models.ForeignKey(User,
                             on_delete=models.PROTECT,
                             related_name='answers',
                             blank=True,
                             null=True)

    option = models.ForeignKey(Option,
                               on_delete=models.CASCADE,
                               related_name='answers',
                               blank=True,
                               null=True)
