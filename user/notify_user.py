import logging

from django.conf import settings
from django.core.mail import send_mail
from smtplib import SMTPException


log = logging.getLogger(__name__)


def notify_user(to_email, message, subject):
    log.debug("Trying to notify_user")

    from_email = settings.SERVER_EMAIL

    to_emails = [to_email]

    try:
        send_mail(subject, message, from_email, to_emails)
    except SMTPException as e:
        log.exception("Failed to notify_list_users: {}".format(e))
    except Exception as e:
        log.exception("Failed to notify_list_users: {}".format(e))
    else:
        log.exception("sent status email to " + str(to_emails))
