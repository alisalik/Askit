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
from .permissions import IsAuthorOrReadOnly


# Create your views here.


class ListQuestionView(generics.ListAPIView):
    queryset = Questions.objects.all().order_by("-created_at")
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated,]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "questions.html"
    lookup_field = "slug"

    def get(self,request,*args,**kwargs):
        queryset = self.get_queryset()
        return Response({'queryset':queryset})

class CreateQuestionView(generics.ListCreateAPIView):
    ''' View to create question'''

    queryset = Questions.objects.all().order_by("-created_at")
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated,]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "questioncreate.html"
    lookup_field = "slug"

    def get(self,request,*args,**kwargs):
        serializer = self.get_serializer()
        return Response({'questions':serializer})

    def create(self,request,*args,**kwargs):
        serializer  = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=self.request.user)
            return redirect('list-ques')
        else:
            return serializer.errors

class RUDQuestionView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Questions.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated,IsAuthorOrReadOnly]
    lookup_field = "slug"


class AnswerCreateView(generics.CreateAPIView):

    '''View to create answer to question'''

    queryset = Answers.objects.all()
    serializer_class =  AnswerSerializer
    permission_classes = [IsAuthenticated,]
    '''renderer_classes = [TemplateHTMLRenderer]
    template_name = "answer.html"

    def list(self,request,*args,**kwargs):
        queryset = self.get_queryset()
        return Response({'answer':queryset})


    def create(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect('questions')'''

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
    permission_classes = [IsAuthenticated,IsAuthorOrReadOnly]
    lookup_field = "uuid"



class AnswerListView(generics.ListAPIView):

    '''View to list all answers to a question'''

    queryset = Answers.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated,]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "answers.html"

    def get_queryset(self):
        kwarg_slug = self.kwargs.get("slug")
        return Answers.objects.filter(question__slug=kwarg_slug).order_by("-created_at")

    def list(self,request,*args,**kwargs):
        queryset = self.get_queryset()
        return Response({'answers':queryset})


class AnswerLikeAPIView(APIView):
    """Allow users to add/remove a like to/from an answer instance."""

    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "uuid"

    def delete(self, request, uuid):
        """Remove request.user from the voters queryset of an answer instance."""
        answer = get_object_or_404(Answers, uuid=uuid)
        user = request.user

        answer.voters.remove(user)
        answer.save()

        serializer_context = {"request": request}
        serializer = self.serializer_class(answer, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, uuid):
        """Add request.user to the voters queryset of an answer instance."""
        answer = get_object_or_404(Answers, uuid=uuid)
        user = request.user

        answer.voters.add(user)
        answer.save()

        serializer_context = {"request": request}
        serializer = self.serializer_class(answer, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)
