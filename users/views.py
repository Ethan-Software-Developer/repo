from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistrationForm, LoginForm, ProfileUpdateForm, UserUpdateForm
from .models import CustomUser, Profile
from .utils import generate_otp, send_otp
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
import random
from django.utils.timezone import now
import uuid
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth.tokens import PasswordResetTokenGenerator



def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Temporarily deactivate user until OTP is verified
            otp = generate_otp()
            request.session['registration_data'] = {
                'email': user.email,
                'password': form.cleaned_data['password'],
                'first_name': user.first_name,
                'last_name': user.last_name,
                'otp': otp,
            }
            send_otp(user.email, otp)
            messages.success(request, "An OTP has been sent to your email.")
            return redirect('verify_otp')
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})




def otp_verification(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        try:
            user = CustomUser.objects.get(email=request.session.get('email'))
            if not user.is_active:
                if user.is_otp_valid():
                    if user.otp == otp:
                        user.is_active = True
                        user.otp = None
                        user.otp_created_at = None  # Clear timestamp
                        user.save()
                        login(request, user)
                        messages.success(request, "Your account has been verified and you're now logged in.")
                        return redirect('dashboard')
                    else:
                        messages.error(request, "Invalid OTP. Please try again.")
                else:
                    messages.error(request, "OTP has expired. Please request a new one.")
                    return redirect('resend_otp')  # Add a route to resend OTP

            else:
                messages.warning(request, "Your account is already verified. Please log in.")
                return redirect('login')
        except ObjectDoesNotExist:
            messages.error(request, "User not found. Please register again.")
            return redirect('register')
    return render(request, 'users/otp_verification.html')



def verify_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        registration_data = request.session.get('registration_data')
        if registration_data and int(otp) == registration_data['otp']:
            user = CustomUser.objects.create_user(
                email=registration_data['email'],
                password=registration_data['password'],
                first_name=registration_data['first_name'],
                last_name=registration_data['last_name']
            )
            user.is_active = True  # Activate the user after successful OTP verification
            user.save()
            messages.success(request, "Your account has been created successfully!")
            del request.session['registration_data']  # Clear session data
            return redirect('login')
        else:
            messages.error(request, "Invalid OTP. Please try again.")
    return render(request, 'users/verify_otp.html')

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, "You are now logged in.")
                    return redirect('dashboard')  # Redirect to the dashboard after successful login
                else:
                    messages.error(request, "Your account is inactive. Please verify your email first.")
                    return redirect('verify_otp')  # Redirect to OTP verification page
            else:
                messages.error(request, "Invalid email or password.")
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})



def resend_otp(request):
    try:
        user = CustomUser.objects.get(email=request.session.get('email'))
        if not user.is_active:
            user.otp = f"{random.randint(100000, 999999)}"
            user.otp_created_at = now()
            user.save()
            # Send the OTP via email (reuse your email-sending logic)
            send_otp(user.email, user.otp)
            messages.success(request, "A new OTP has been sent to your email.")
        else:
            messages.warning(request, "Your account is already verified. Please log in.")
            return redirect('login')
    except ObjectDoesNotExist:
        messages.error(request, "User not found. Please register again.")
        return redirect('register')
    return redirect('otp_verification')




def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')  # Redirect to login page


@login_required
def dashboard(request):
    # Fetch user profile if it exists
    profile = None
    if hasattr(request.user, 'profile'):
        profile = request.user.profile

    # Custom data based on the user
    user_data = {
        "first_name": request.user.first_name,
        "last_name": request.user.last_name,
        "email": request.user.email,
        "role": request.user.groups.first().name if request.user.groups.exists() else "Student",
        "profile_picture": profile.profile_picture.url if profile and profile.profile_picture else None,
    }

    return render(request, "users/dashboard.html", {"user_data": user_data})


def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get('email')
        try:
            user = CustomUser.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = request.build_absolute_uri(reverse('reset_password', kwargs={'uidb64': uid, 'token': token}))


            # Send Reset Email
            send_mail(
                'Password Reset Request',
                f'Click the link to reset your password: {reset_link}',
                'noreply@aurum.com',
                [email],
                fail_silently=False,
            )
            messages.success(request, 'A password reset link has been sent to your email.')
            return redirect('forgot_password')
        except CustomUser.DoesNotExist:
            messages.error(request, 'Email not found.')
    
    return render(request, 'users/forgot_password.html')



def reset_password(request, uidb64=None, token=None):
    if request.method == 'POST':
        new_password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect(request.path)
        
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = CustomUser.objects.get(pk=uid)
            token_generator = PasswordResetTokenGenerator()
            
            if token_generator.check_token(user, token):
                user.set_password(new_password)
                user.save()
                messages.success(request, "Password reset successfully.")
                return redirect('login')
            else:
                messages.error(request, "The reset link is invalid or has expired.")
        except Exception:
            messages.error(request, "Invalid reset link.")
            
    return render(request, 'users/reset_password.html')


@login_required
def profile(request):
    # Automatically create a profile for the user if it doesn't exist
    if not hasattr(request.user, 'profile'):
        Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile has been successfully updated!")
            return redirect("profile")
        else:
            # Add error messages if the forms are not valid
            messages.error(request, "Please correct the errors below.")
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
    }
    return render(request, "users/profile.html", context)
