from django.contrib.auth import views as auth_views
from django.urls import path
from . import views


app_name = 'cookiejar'

# Cookiejar urls
urlpatterns = [
    path('login/', views.CookieJarView.as_view(), name='login'),
]
