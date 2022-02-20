from django.urls import path,include
from questions.views import QuestionViewset,AnswerCreateView,AnsDelUpdView,AnswerListView
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register(r"questions",QuestionViewset)

urlpatterns=[
    path("",include(router.urls)),
    path("questions/<slug:slug>/answer/",AnswerCreateView.as_view(),name='create-ans'),
    path("answers/<uuid:uuid>",AnsDelUpdView.as_view(),name='answer-update'),
    path("questions/<slug:slug>/listans/",AnswerListView.as_view(),name='list-answer'),
]
