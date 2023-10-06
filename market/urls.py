from django.urls import path
from . import views

urlpatterns = [
    # root home path
    path('', views.home, name='home'),
]
