from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

from config.settings import CACHE_ENABLED
from .models import MailingAttempt, Mailing, Recipient, Message


def send_mailing(mailing_id):
    mailing = Mailing.objects.get(id=mailing_id)
    if mailing.status != "started":
        mailing.status = "started"
        mailing.save()

    for recipient in mailing.recipients.all():
        try:
            send_mail(
                subject=mailing.message.mail_topic,
                message=mailing.message.text,
                from_email=None,
                recipient_list=[recipient.email],
                fail_silently=False,
            )
            MailingAttempt.objects.create(
                mailing=mailing,
                status="successfully",
                attempt_at=timezone.now(),
                server_response="OK",
            )
        except Exception as e:
            MailingAttempt.objects.create(
                mailing=mailing,
                status="unsuccessfully",
                attempt_at=timezone.now(),
                server_response=str(e),
            )

    if timezone.now() > mailing.send_end:
        mailing.status = "completed"
        mailing.save()


def get_recipient_from_cache():
    if not CACHE_ENABLED:
        return Recipient.objects.all()
    key = "recipient_list"
    recipients = cache.get(key)
    if recipients is not None:
        return recipients
    recipients = Recipient.objects.all()
    cache.set(key, recipients)
    return recipients


def get_message_from_cache():
    if not CACHE_ENABLED:
        return Message.objects.all()
    key = "message_list"
    messages = cache.get(key)
    if messages is not None:
        return messages
    messages = Message.objects.all()
    cache.set(key, messages)
    return messages


def get_mailing_from_cache():
    if not CACHE_ENABLED:
        return Mailing.objects.all()
    key = "mailing_list"
    mailings = cache.get(key)
    if mailings is not None:
        return mailings
    mailings = Mailing.objects.all()
    cache.set(key, mailings)
    return mailings
