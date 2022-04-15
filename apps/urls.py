from django.urls import path
from django.contrib.auth import views as auth_view
from apps import views

urlpatterns = [
    path('signup/',views.SignupView.as_view(),name='signup'),

    path('login/',auth_view.LoginView.as_view(
        template_name='apps/registration/login.html'),name='login'),

    path('logout/',auth_view.LogoutView.as_view(),name='logout'),

    path('password_reset/',auth_view.PasswordResetView.as_view(
       template_name='apps/registration/password_reset.html'),name='password_reset'),

    path('password_reset/done/',auth_view.PasswordResetDoneView.as_view(
        template_name='apps/registration/password_reset_done.html'),name='password_reset_done'),

    path('reset/<uidb64>/<token>/',auth_view.PasswordResetConfirmView.as_view(
        template_name='apps/registration/password_reset_confirm.html'),name='password_reset_confirm'),

    path('reset/done/',auth_view.PasswordResetCompleteView.as_view(
        template_name='apps/registration/password_reset_complete.html'),name='password_reset_complete'),
    
    path('activation/',views.activate_message),
    path('activation_done/',views.activation_done),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'), 
]
