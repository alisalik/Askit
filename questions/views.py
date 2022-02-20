from django.shortcuts import render,redirect
from rest_framework import viewsets,generics,status
from rest_framework.response import Response
from questions.models import Questions,Answers
from questions.serializers import QuestionSerializer,AnswerSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.renderers import TemplateHTMLRenderer


# Create your views here.


class QuestionViewset(ModelViewSet):
    ''' Viewset to create question'''

    queryset = Questions.objects.all().order_by("-created_at")
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated,]
    lookup_field = "slug"

    def perform_create(self,serializer):
        serializer.save(author=self.request.user)

class AnswerCreateView(generics.CreateAPIView):

    '''View to create answer to question'''

    queryset = Answers.objects.all()
    serializer_class =  AnswerSerializer
    permission_classes = [IsAuthenticated,]

    def perform_create(self,serializer):
        kwarg_slug = self.kwargs.get("slug")  #gets the slug for the specific question
        question = get_object_or_404(Questions,slug = kwarg_slug)

        if question.answers.filter(author=self.request.user).exists():
            raise ValidationError("you have already answered this question")

        serializer.save(author=self.request.user,question=question)

class AnsDelUpdView(generics.RetrieveUpdateDestroyAPIView):

    '''View to delete update an answer'''

    queryset = Answers.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated,]
    lookup_field = "uuid"


class AnswerListView(generics.ListAPIView):

    '''View to list all answers to a question'''

    queryset = Answers.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        kwarg_slug = self.kwargs.get("slug")
        return Answers.objects.filter(question__slug=kwarg_slug).order_by("-created_at")
