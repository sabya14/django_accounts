from __future__ import absolute_import, unicode_literals
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
import celery

User = get_user_model()
@celery.task
def print_hello():
    print ('hello there')\

@celery.task
def activation_mail_send(user_id):
    user = User.objects.get(id=user_id)
    subject = 'Hello {name}:{email}'.format(name=user.get_full_name(),email =user.email)
    message = 'Click on the link to activate -{url}.{id}'.format(url='url',id=user.id)
    send_mail(subject=subject,message=message,from_email=settings.DEFAULT_EMAIL_FROM,recipient_list=[user.email])