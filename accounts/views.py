from django.shortcuts import render,redirect
from rest_framework import generics,mixins,viewsets
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from accounts.models import UserProfile
from accounts.serializers import UserSerializer
from rest_framework.response import Response
from accounts.permissions import UpdateOwnProfile
from rest_framework.renderers import TemplateHTMLRenderer
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout



# Create your views here.

class RegisterViewset(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer
    #permission_classes=[UpdateOwnProfile,]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'Register.html'

    def list(self,request,*args,**kwargs):
        serializer = self.get_serializer()
        return Response({'serializer':serializer})

    def create(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect('login')
        else:
            return Response(serializer.errors)

def dashboard(request):
    return render(request,'dboard.html')


def loginView(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            print(user)
            login(request, user)
            return redirect('dboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})
    #return render(request,'login.html')

def logoutView(request):
    logout(request)
    return redirect("login")
