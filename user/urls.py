from django.urls import path
from .views import RegisterView, LoginView, UsersView

urlpatterns = [

    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('users/', UsersView.as_view()),

]