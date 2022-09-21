from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('log/', views.LogView.as_view(), name='log'),
    path('findindex/', views.FindIndexView.as_view(), name='findindex'),
    path('sendmail/', views.SendMailView.as_view(), name='sendmail'),
]
