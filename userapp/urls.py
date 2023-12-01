from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home),
    path('login',views.login),
    path('register', views.register),
    path('ipdisplay/',views.ipdisp),
    path('users/',views.usersdisp),
    path('users/<int:user_id>/', views.usersdisplay),
    path('scan-ip/',views.some_view),
    path('enrich-ip/<str:ip>/',views.enrichip),
    #path('search/<str:query>',views.search_elasticsearch),
    path('search/<str:query>/', views.StatusSuccessAPIView.as_view()),
]