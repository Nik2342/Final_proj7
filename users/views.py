from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView
from django.core.checks import messages
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
import secrets

from config.settings import EMAIL_HOST_USER
from mailing.models import Mailing
from users.forms import UserRegisterForm
from users.models import User


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/email_confirm/{token}/"
        send_mail(
            subject="Подтверждение почты",
            message=f"Привет, перейди по ссылке для подтверждения почты {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)

    def block_user(request, pk):
        block_user = get_object_or_404(User, pk=pk)
        if not request.user.has_per("users.can_block_user"):
            raise PermissionDenied
        else:
            block_user.is_active = False
            block_user.save()
        return redirect(reverse("mailing:home"))

    def disable_mailing(request, mailing_id):
        mailing = get_object_or_404(Mailing, pk=mailing_id)
        mailing.status = "completed"
        mailing.save()
        messages.success(request, f"Рассылка #{mailing.id} отключена")
        return redirect("mailing:mailing_list")


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    if user.is_active:
        messages.warning(request, "Ваш аккаунт уже активирован")
    else:
        user.is_active = True
        user.token = None
        user.save()
        messages.success(request, "Ваш аккаунт успешно активирован!")
    return redirect(reverse("users:login"))
