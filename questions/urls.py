from django.urls import path,include
from questions.views import AnswerCreateView,AnsDelUpdView,AnswerListView,ListQuestionView,CreateQuestionView,AnswerLikeAPIView,RUDQuestionView
from rest_framework.routers import DefaultRouter

'''router=DefaultRouter()
router.register(r"questions",QuestionViewset)'''

urlpatterns=[
    #path("",include(router.urls)),
    path("questions/",ListQuestionView.as_view(),name='list-ques'),
    path("quescreate/",CreateQuestionView.as_view(),name='create-ques'),
    path("question/<slug:slug>/",RUDQuestionView.as_view(),name = 'question-update'),
    path("questions/<slug:slug>/answer/",AnswerCreateView.as_view(),name='create-ans'),
    path("answers/<uuid:uuid>",AnsDelUpdView.as_view(),name='answer-update'),
    path("questions/<slug:slug>/listans/",AnswerListView.as_view(),name='list-answer'),
    path("answer/<uuid:uuid>/like",AnswerLikeAPIView.as_view(),name = 'like')

]
