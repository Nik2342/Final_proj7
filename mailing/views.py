from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)

from mailing.forms import RecipientForm, MessageForm, MailingForm
from mailing.models import Recipient, Message, Mailing, MailingAttempt
from mailing.services import (
    get_recipient_from_cache,
    get_message_from_cache,
    get_mailing_from_cache,
)


class MessageListView(ListView):
    model = Message

    def get_queryset(self):
        return get_message_from_cache()


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = "mailing/message_form.html"
    success_url = reverse_lazy("mailing:message_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = "mailing/message_form.html"
    success_url = reverse_lazy("mailing:message_list")


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy("mailing:message_list")


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = "mailing/message_detail.html"


class RecipientListView(ListView):
    model = Recipient

    def get_queryset(self):
        return get_recipient_from_cache()


class RecipientCreateView(LoginRequiredMixin, CreateView):
    model = Recipient
    form_class = RecipientForm
    template_name = "mailing/recipient_form.html"
    success_url = reverse_lazy("mailing:recipient_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class RecipientUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipient
    form_class = RecipientForm
    template_name = "mailing/recipient_form.html"
    success_url = reverse_lazy("mailing:recipient_list")


class RecipientDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipient
    success_url = reverse_lazy("mailing:recipient_list")


class RecipientDetailView(LoginRequiredMixin, DetailView):
    model = Recipient
    template_name = "mailing/recipient_detail.html"


class MailingListView(ListView):
    model = Mailing

    def get_queryset(self):
        return get_mailing_from_cache()


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mailing/mailing_form.html"
    success_url = reverse_lazy("mailing:mailing_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = "mailing/mailing_detail.html"


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mailing/mailing_form.html"
    success_url = reverse_lazy("mailing:mailing_list")


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy("mailing:mailing_list")


def home(request):
    total_mailings = Mailing.objects.count()
    active_mailings = Mailing.objects.filter(status="started").count()
    unique_clients = Recipient.objects.values("email").distinct().count()

    context = {
        "total_mailings": total_mailings,
        "active_mailings": active_mailings,
        "unique_clients": unique_clients,
    }
    return render(request, "mailing/home.html", context)


class StatisticsView(TemplateView):
    template_name = "mailing/statistics.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        mailings = Mailing.objects.filter(owner=self.request.user)

        attempts = MailingAttempt.objects.filter(mailing__in=mailings)
        success_attempts = attempts.filter(status="successfully").count()
        failed_attempts = attempts.filter(status="unsuccessfully").count()

        mailing_stats = []
        for mailing in mailings:
            attempts = mailing.attempts.all()
            mailing_stats.append(
                {
                    "mailing": mailing,
                    "success_count": attempts.filter(status="successfully").count(),
                    "failed_count": attempts.filter(status="unsuccessfully").count(),
                    "total_count": attempts.count(),
                }
            )

        context.update(
            {
                "success_attempts": success_attempts,
                "failed_attempts": failed_attempts,
                "mailing_stats": mailing_stats,
            }
        )
        return context
