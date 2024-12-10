import random
from datetime import datetime
from django.conf import settings
from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string

def get_random_string_code():
    return str(random.randint(100000, 999999))

def custom_send_mail(to_email, code):
    text_content = render_to_string(
        template_name="accounts/password_reset_email.html",
        context={"receiver_name": to_email,
                "code": code},
        )
    
    email = EmailMessage(
            subject="Parolni tiklash uchun kod",
            body=text_content,
            to=[to_email],
        )
    email.content_subtype = "html"
    email.send()