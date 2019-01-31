from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

app_name = 'challenge'

# Decipher challenge urls
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('home/', views.HomeView.as_view(), name='home'),
    path('challenge/', views.ChallengeView.as_view(), name='challenge'),
    path('rules/', views.RulesView.as_view(), name='rules'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('ranking/', views.RankingView.as_view(), name='ranking'),
    path('password_change/',
         auth_views.PasswordChangeView.as_view(template_name='challenge/password_change.html'),
         name='password_change'),
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='challenge/password_change_done.html'),
         name='password_change_done'),
    path('password_reset/',
         auth_views.PasswordResetView.as_view(template_name='challenge/password_reset.html'),
         name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='challenge/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='challenge/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='challenge/password_reset_complete.html'),
         name='password_reset_complete'),
]
