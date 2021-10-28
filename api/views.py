from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Prefetch
from rest_framework import viewsets
from rest_framework.response import Response

from .serializers import (
    UserSerializer,
    PollSerializer,
    AnswerSerializer,
    OptionSerializer,
    QuestionSerializer,
    PollWithUserAnswersSerializer,
)

from .models import Poll, Question, Answer, Option
from .permissions import IsAdminUserOrReadOnly


class PollViewSet(viewsets.ModelViewSet):
    serializer_class = PollSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    queryset = Poll.objects.filter(start_at__isnull=False,
                                   finish_at__isnull=True)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    queryset = User.objects.all()


class AnswerViewSet(viewsets.ModelViewSet):
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()


class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    queryset = Question.objects.all()


class OptionViewSet(viewsets.ModelViewSet):
    serializer_class = OptionSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    queryset = Option.objects.all()


class PollWithUserAnswersViewSet(viewsets.ViewSet):
    serializer_class = Poll
    permission_classes = [IsAdminUserOrReadOnly]

    def list(self, request, user_pk=None):
        user_answers = Answer.objects.filter(user=user_pk)
        polls_id = [answer.poll.id for answer in user_answers]
        queryset = Poll.objects.prefetch_related(
            Prefetch(
                'answers',
                queryset=user_answers
            )
        ).filter(id__in=polls_id)
        serializer = PollWithUserAnswersSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request,  pk=None, user_pk=None):
        queryset = Poll.objects.prefetch_related(
            Prefetch(
                'answers',
                queryset=Answer.objects.filter(user=user_pk)
            )
        )
        answer = get_object_or_404(queryset, pk=pk)
        serializer = PollWithUserAnswersSerializer(answer)
        return Response(serializer.data)
