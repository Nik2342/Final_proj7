from datetime import datetime
from django.db import models
from django.db.models import ForeignKey, ManyToManyField

from users.models import User


class Recipient(models.Model):
    email = models.CharField(unique=True, verbose_name="Email")
    name = models.CharField(blank=True, null=True, verbose_name="Ф. И. О.")
    comment = models.TextField(blank=True, null=True, verbose_name="Комментарий")
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Получатель"
        verbose_name_plural = "Получатели"
        permissions = [
            ("can_see_recipient", "Can see recipient"),
        ]

    def __str__(self):
        return self.email


class Message(models.Model):
    mail_topic = models.CharField(blank=True, null=True, verbose_name="Тема письма")
    text = models.TextField(blank=True, null=True, verbose_name="Текст письма")
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Письмо"
        verbose_name_plural = "Письма"

    def __str__(self):
        return self.mail_topic


class Mailing(models.Model):

    STATUS_CHOICES = [
        ("created", "Создана"),
        ("started", "Запущена"),
        ("completed", "Завершена"),
    ]
    first_send_at = models.DateTimeField(
        default=datetime.now, verbose_name="Дата и время первой отправки"
    )
    send_end = models.DateTimeField(verbose_name="Дата и время окончания отправки")
    status = models.CharField(
        choices=STATUS_CHOICES, default="created", verbose_name="Статус"
    )
    message = ForeignKey(Message, on_delete=models.SET_NULL, null=True, blank=True)
    recipients = ManyToManyField(
        Recipient,
        blank=True,
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        permissions = [
            ("can_see_mailing", "Can see mailing"),
        ]


class MailingAttempt(models.Model):
    SUCCESS = "success"
    FAILURE = "failure"
    STATUS_CHOICES = [
        (SUCCESS, "Успешно"),
        (FAILURE, "Неуспешно"),
    ]
    attempt_at = models.DateTimeField(
        blank=True, null=True, verbose_name="Дата и время попытки"
    )
    status = models.CharField(
        blank=True, null=True, choices=STATUS_CHOICES, verbose_name="Статус"
    )
    server_response = models.TextField(
        blank=True, null=True, verbose_name="Ответ почтового сервера"
    )
    mailing = ForeignKey(
        Mailing,
        on_delete=models.CASCADE,
        verbose_name="Рассылка",
        related_name="attempts",
    )

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылок"
        ordering = ["attempt_at"]
