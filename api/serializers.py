from rest_framework import serializers
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer
from django.contrib.auth.models import User

from .models import Poll, Question, Option, Answer


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff']


class PollSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Poll
        fields = ['id', 'title', 'description', 'start_at', 'finish_at']


class OptionSerializer(serializers.HyperlinkedModelSerializer):
    question_id = serializers.IntegerField()

    class Meta:
        model = Option
        fields = ['id', 'text', 'question_id']


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    poll_id = serializers.IntegerField()

    class Meta:
        model = Question
        fields = ['id', 'text', 'type', 'poll_id']


class AnswerSerializer(serializers.HyperlinkedModelSerializer):
    option = OptionSerializer(read_only=True)
    question = QuestionSerializer(read_only=True)

    user_id = serializers.IntegerField(required=False)
    poll_id = serializers.IntegerField(write_only=True)
    question_id = serializers.IntegerField(write_only=True)
    option_id = serializers.IntegerField(required=False, write_only=True)

    class Meta:
        model = Answer
        fields = ['id', 'user_id', 'poll_id', 'question_id', 'question_id',
                  'option_id', 'text_form', 'option', 'question']


class PollWithUserAnswersSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'user_pk': 'user__pk',
    }
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Poll
        fields = ['id', 'title', 'description', 'start_at', 'finish_at',
                  'answers']


