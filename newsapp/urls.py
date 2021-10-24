from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('',views.home,name="home"),
    path('search/',views.search, name="search"),
    path('login/',views.log_in,name="login"),
    path('signup/',views.sign_up,name="signup"),
    path('logout/',views.log_out,name="logout"),
    path('addnews/',views.addnews,name="addnews"),
    path('uploadnews/',views.uploadnews,name="uploadnews"),
    path('comments/',views.comment.as_view(),name="comments"),
    path('news/<str:sha>/',views.news,name="news"),
    path('<str:cat>/',views.category,name="category"),
]