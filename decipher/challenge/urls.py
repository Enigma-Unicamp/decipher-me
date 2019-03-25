from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from . import forms


app_name = 'challenge'

# Decipher challenge urls
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('home/', views.HomeView.as_view(), name='home'),
    path('challenges_page/',
         views.ChallengesPageView.as_view(),
         name='challenges_page'
        ),
    path('challenge/', views.ChallengeView.as_view(), name='challenge'),
    path('rules/', views.RulesView.as_view(), name='rules'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('ranking/', views.RankingView.as_view(), name='ranking'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('password_change/', views.PasswordChangeView.as_view(),
         name='password_change'
        ),

    # password reset module (lost password)
    path('password_reset/',
         auth_views.PasswordResetView.as_view(
             template_name='challenge/password_reset.html'
         ),
         name='password_reset'
        ),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='challenge/password_reset_done.html'
         ),
         name='password_reset_done'
        ),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             form_class=forms.PasswordResetConfirmForm,
             template_name='challenge/password_reset_confirm.html'
         ),
         name='password_reset_confirm'
        ),
    path('reset/done/',
         views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'
        ),
]
