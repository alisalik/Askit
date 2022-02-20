from django.urls import path,include
from rest_framework.routers import DefaultRouter
from accounts.views import RegisterViewset,loginView,logoutView,dashboard

router = DefaultRouter()
router.register(r"register",RegisterViewset)

urlpatterns= [
    path("",include(router.urls)),
    path('login/',loginView,name='login'),
    path('logout/',logoutView,name='logout'),
    path('dashboard',dashboard,name='dboard')

]
