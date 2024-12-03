import random
from django.core.mail import send_mail
from django.conf import settings

def generate_otp():
    return random.randint(100000, 999999)

def send_otp(email, otp):
    subject = "Your OTP Verification Code"
    message = f"Your OTP code is {otp}. Please enter this code to verify your email."
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email])
