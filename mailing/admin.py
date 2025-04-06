from django.contrib import admin

from mailing.models import Mailing, Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("mail_topic",)
