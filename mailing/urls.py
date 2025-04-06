from django.urls import path, include

from mailing import views
from mailing.apps import MailingConfig
from mailing.views import StatisticsView

app_name = MailingConfig.name

urlpatterns = [
    path("", views.home, name="home"),
    path("message/", views.MessageListView.as_view(), name="message_list"),
    path("message/create/", views.MessageCreateView.as_view(), name="message_create"),
    path(
        "message/<int:pk>/update/",
        views.MessageUpdateView.as_view(),
        name="message_update",
    ),
    path(
        "message/<int:pk>/delete/",
        views.MessageDeleteView.as_view(),
        name="message_delete",
    ),
    path(
        "message/<int:pk>/detail/",
        views.MessageDetailView.as_view(),
        name="message_detail",
    ),
    path("mailing/", views.MailingListView.as_view(), name="mailing_list"),
    path("mailing/create/", views.MailingCreateView.as_view(), name="mailing_create"),
    path("mailing/<int:pk>/", views.MailingDetailView.as_view(), name="mailing_detail"),
    path(
        "mailing/<int:pk>/update/",
        views.MailingUpdateView.as_view(),
        name="mailing_update",
    ),
    path(
        "mailing/<int:pk>/delete/",
        views.MailingDeleteView.as_view(),
        name="mailing_delete",
    ),
    path(
        "mailing/<int:pk>/detail/",
        views.MailingDetailView.as_view(),
        name="mailing_detail",
    ),
    path("recipient/", views.RecipientListView.as_view(), name="recipient_list"),
    path(
        "recipient/create/",
        views.RecipientCreateView.as_view(),
        name="recipient_create",
    ),
    path(
        "recipient/<int:pk>/update/",
        views.RecipientUpdateView.as_view(),
        name="recipient_update",
    ),
    path(
        "recipient/<int:pk>/delete/",
        views.RecipientDeleteView.as_view(),
        name="recipient_delete",
    ),
    path(
        "recipient/<int:pk>/detail/",
        views.RecipientDetailView.as_view(),
        name="recipient_detail",
    ),
    path("statistics/", StatisticsView.as_view(), name="statistics"),
]
