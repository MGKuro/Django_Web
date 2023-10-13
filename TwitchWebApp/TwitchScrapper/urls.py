from django.urls import path
from . import views


urlpatterns = [
    path("start", views.Start_Scrapping, name = "start"),
    path("", views.Empty, name = "home")
    ]