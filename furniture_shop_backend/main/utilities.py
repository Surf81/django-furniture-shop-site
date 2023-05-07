from datetime import datetime
from os.path import splitext
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail
from smtplib import SMTPDataError, SMTPRecipientsRefused
from django.http import Http404


def get_timestamp_path(instance, filename):
    return '{!s:s}{!s:s}'.format(datetime.now().timestamp(), splitext(filename)[1])


def send_claim_notification(comment):
    if settings.ALLOWED_HOSTS and settings.ALLOWED_HOSTS[0] not in ('localhost', '127.0.0.1'):
        host = 'http://' + settings.ALLOWED_HOSTS[0]
    else:
        host = 'http://127.0.0.1:8000'


    context = {
               'host': host, 
               'comment': comment
              }
    subject = render_to_string('email/claim_letter_subject.txt', context)
    body_text = render_to_string('email/claim_letter_body.txt', context)

    try:
        send_mail(subject, body_text, settings.EMAIL_HOST_USER, [settings.QUALITY_CONTROL_SERVISE_EMAIL])
    except (SMTPDataError, SMTPRecipientsRefused) as e:
        print('log. error', e)



def user_is_staff(user):
    return user.is_staff


def user_permission_test(condition):
    def wrapper(func):
        def get_controller(request, *args, **kwargs):
            if condition(request.user):
                return func(request, *args, **kwargs)
            else:
                raise Http404
        return get_controller
    return wrapper

