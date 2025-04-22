from django.core.exceptions import ValidationError
from django.forms import ModelForm, BooleanField

from mailing.models import Recipient, Message, Mailing


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"


class RecipientForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Recipient
        fields = ["email", "name", "comment"]
        exclude = ["owner"]


class MessageForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Message
        fields = ["mail_topic", "text"]
        exclude = ["owner"]


class MailingForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Mailing
        fields = ["first_send_at", "send_end", "status", "message", "recipients"]
        exclude = ["owner"]
