from django.core.mail import BadHeaderError
from django.conf import settings
# from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
import os
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


def send_email(email, uid, username):
    # //EMAIL VARS
    # create email arguments
    subject = 'Activate your account on OSTPlace!'
    to_email = email
    from_email = os.environ.get('EMAIL_HOST_USER')
    domain = os.environ.get('FRONTEND_URL_ACTIVATE')
    uidGood = force_str(urlsafe_base64_decode(uid))
    user = User.objects.get(id=uidGood)
    token = Token.objects.get(user=user)
    template = render_to_string('emailTemplate.html', {'token': token,
                                                       'domain': domain,
                                                       'username': username})
    # send email
    if subject and template and from_email:
        try:
            msg = EmailMultiAlternatives(subject, template, from_email, [to_email])
            msg.attach_alternative(template, "text/html")
            msg.send()
            print('User confirm has flew away')

        except BadHeaderError:
            print('ERROR Header')
            return BadHeaderError


def change_email(oldEmail, newEmail, token, username):
    # //EMAIL VARS
    # create email arguments
    subject = 'Change your email on OSTPlace'
    to_email = oldEmail
    from_email = os.environ.get('EMAIL_HOST_USER')
    domain = os.environ.get('FRONTEND_URL')
    template = render_to_string('ChangeEmailTemplate.html', {'domain': domain,
                                                             'username': username,
                                                             'newEmail': newEmail,
                                                             'token': token})
    # send email
    if subject and template and from_email:
        try:
            msg = EmailMultiAlternatives(subject, template, from_email, [to_email])
            msg.attach_alternative(template, "text/html")
            print('SENT TO:', to_email)
            msg.send()
            print('User change email bird has flew away')

        except BadHeaderError:
            print('ERROR Header')
            return BadHeaderError


def alreadyChanged_email(email, username):
    # //EMAIL VARS
    # create email arguments
    subject = 'Email changed on OSTPlace'
    to_email = email
    from_email = os.environ.get('EMAIL_HOST_USER')
    domain = os.environ.get('FRONTEND_URL')
    template = render_to_string('EmailChanged.html', {'domain': domain,
                                                      'username': username,
                                                      'email': email})
    # send email
    if subject and template and from_email:
        try:
            msg = EmailMultiAlternatives(subject, template, from_email, [to_email])
            msg.attach_alternative(template, "text/html")
            msg.send()
            print('User change email bird has flew away')

        except BadHeaderError:
            print('ERROR Header')
            return BadHeaderError