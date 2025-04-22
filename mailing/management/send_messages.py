from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings
from mailing.models import Mailing, MailingAttempt


class Command(BaseCommand):
    help = "Отправка почтовых рассылок получателям"

    def handle(self, *args, **kwargs):
        mailings = Mailing.objects.filter(status__in=["created", "started"])

        for mailing in mailings:
            self.stdout.write(f"Обработка рассылки ID {mailing.id}...")

            if not hasattr(mailing, "message") or not mailing.recipients.exists():
                self.stdout.write(
                    f"В рассылке ID {mailing.id} отсутствует сообщение или получатели"
                )
                continue

            for recipient in mailing.recipients.all():
                try:
                    send_mail(
                        mailing.message.mail_topic,
                        mailing.message.text,
                        settings.EMAIL_HOST_USER,
                        [recipient.email],
                        fail_silently=False,
                    )

                    MailingAttempt.objects.create(
                        mailing=mailing,
                        status="successfully",
                        attempt_at=timezone.now(),
                        server_response="Email отправлен",
                    )
                    self.stdout.write(
                        f"Сообщение '{mailing.message.mail_topic}' успешно отправлено на {recipient.email}"
                    )

                except Exception as e:
                    MailingAttempt.objects.create(
                        mailing=mailing,
                        status="unsuccessfully",
                        attempt_at=timezone.now(),
                        server_response=str(e),
                    )
                    self.stdout.write(
                        self.style.ERROR(
                            f"Ошибка при отправке на {recipient.email}: {str(e)}"
                        )
                    )

            mailing.status = "started"
            mailing.save()
