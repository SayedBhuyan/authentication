from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import generic
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import LogoutRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetCompleteView,
    PasswordResetDoneView,
    PasswordResetConfirmView
)


from .forms import (
    LoginForm,
    UserRegistrationForm,
    ChangePasswordForm,
    SendEmailForm,
    AccountSetPasswordForm
)


@method_decorator(never_cache, name="dispatch")
class Home(LoginRequiredMixin, generic.TemplateView):
    login_url = "login"
    template_name = 'account/home.html'

@method_decorator(never_cache, name="dispatch")
class Login(LogoutRequiredMixin, generic.View):
    def get(self, *args, **kwargs):

        context = {
            "form": LoginForm()
        }

        return render(self.request, "account/login.html", context)

    def post(self, *args, **kwargs):
        
        form = LoginForm(self.request.POST)


        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data.get("username"),
                password=form.cleaned_data.get("password")
            )

            if user:
                login(self.request, user)
                return redirect("home")
            else:
                messages.warning(self.request, "Wrong Credintials")
    
        return render(self.request, "account/login.html", {"form": form})
    
class Logout(generic.View):
    def get(self, *args, **kwargs):
        logout(self.request)
        return redirect("login")


@method_decorator(never_cache, name="dispatch")
class Registration(LogoutRequiredMixin, generic.CreateView):
    template_name = "account/registration.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        messages.success(self.request, "Registration Successful!")
        return super().form_valid(form)


@method_decorator(never_cache, name="dispatch")
class ChangePassword(LoginRequiredMixin, generic.FormView):
    template_name = "account/change_password.html"
    form_class = ChangePasswordForm
    login_url = reverse_lazy("login")
    success_url = reverse_lazy("login")

    def get_form_kwargs(self):
        context = super().get_form_kwargs()
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        user = self.request.user
        user.set_password(form.cleaned_data.get("new_password1"))
        user.save()
        messages.success(self.request, "Password has been changed.")
        return super().form_valid(form)

class SendEmailToResetPassword(PasswordResetView):
    template_name = "account/password_reset.html"
    form_class = SendEmailForm

class ViewPasswordResetComplete(PasswordResetCompleteView):
    template_name = "account/password_reset_complete.html"
    title = ("Password reset complete")

class ViewPasswordResetDone(PasswordResetDoneView):
    template_name = "account/password_reset_done.html"
    title = ("Password reset sent")

@method_decorator(never_cache, name="dispatch")
class ViewPasswordResetConfirm(PasswordResetConfirmView):
    form_class = AccountSetPasswordForm
    # post_reset_login = False
    # post_reset_login_backend = None
    # reset_url_token = "set-password"
    template_name = "account/password_reset_confirm.html"
    title = ("Enter new password")
    success_url = reverse_lazy("password_reset_complete")
    # token_generator = default_token_generators