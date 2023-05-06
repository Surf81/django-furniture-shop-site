from django.template.loader import render_to_string
from django.core.signing import Signer
from smtplib import SMTPDataError, SMTPRecipientsRefused

from furniture_shop.settings import ALLOWED_HOSTS


signer = Signer()

def send_activation_notification(user):
    if ALLOWED_HOSTS and ALLOWED_HOSTS[0] not in ('localhost', '127.0.0.1'):
        host = 'http://' + ALLOWED_HOSTS[0]
    else:
        host = 'http://127.0.0.1:8000'
    

    print(signer.sign(user.email))
    print(type(signer.sign(user.email)))

    context = {'user': user, 
               'host': host, 
               'sign': signer.sign(user.email)
               }
    subject = render_to_string('email/activation_letter_subject.txt', context)
    body_text = render_to_string('email/activation_letter_body.txt', context)
    try:
        user.email_user(subject, body_text)
    except (SMTPDataError, SMTPRecipientsRefused) as e:
        print('log. error', e)


        