from django.urls import path, include
from .views import (
    Home,
    Login,
    Logout,
    Registration,
    ChangePassword,
    SendEmailToResetPassword,
    ViewPasswordResetComplete,
    ViewPasswordResetDone,
    ViewPasswordResetConfirm
)
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("login/", Login.as_view(), name="login"),
    path("logout/", Logout.as_view(), name="logout"),
    path("registration/", Registration.as_view(), name="registration"),
    path("change_password/", ChangePassword.as_view(), name="change_password"),
    path("password_reset/", SendEmailToResetPassword.as_view(), name="password_reset"),
    path("password_reset/done/", ViewPasswordResetDone.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", ViewPasswordResetConfirm.as_view(), name="password_reset_confirm"),
    path("reset/done/", ViewPasswordResetComplete.as_view(), name="password_reset_complete"),
]


# accounts/password_reset/ [name='password_reset']
# accounts/password_reset/done/ [name='password_reset_done']
# accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
# accounts/reset/done/ [name='password_reset_complete']
