from datetime import datetime
from os.path import splitext
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail


def get_timestamp_path(instance, filename):
    return '{!s:s}{!s:s}'.format(datetime.now().timestamp(), splitext(filename)[1])


def send_claim_notification(comment):
    if settings.ALLOWED_HOSTS:
        host = 'http://' + settings.ALLOWED_HOSTS[0]
    else:
        host = 'http://localhost:8000'

    context = {'host': host, 'comment': comment}
    subject = render_to_string('email/claim_letter_subject.txt', context)
    body_text = render_to_string('email/claim_letter_body.txt', context)

    send_mail(subject, body_text, settings.EMAIL_HOST_USER, [settings.QUALITY_CONTROL_SERVISE_EMAIL])


def user_is_staff(user):
    return user.is_staff
