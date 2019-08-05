from django.contrib.auth import views as auth_views
from django.urls import path
from . import views


app_name = 'goodsurprise'

# GoodSurprise urls
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login/', views.GoodSurpriseView.as_view(), name='login'),
]
