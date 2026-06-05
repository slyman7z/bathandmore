from django.shortcuts import redirect, render
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.decorators import login_required
# verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage



# Create your views here.
def registration(request):
    
    if request.method == 'POST':
        
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone = request.POST.get('phone')  # Get phone number from POST data
            username = email.split('@')[0]  # Generate username from email
            password = form.cleaned_data['password']
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, phone=phone, username=username, password=password)  
            user.save()
            # user activation
            current_site = get_current_site(request)
            mail_subject = 'Please Activate your account'
            message = render_to_string('auth/account_verification_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            
            # messages.success(request, 'Registration successful. Please check your email to activate your account.')
            
            return redirect('/accounts/login/?command=verification&email=' + email)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegistrationForm()
        
       
    context = {
        'form': form
    }
    return render(request, 'auth/registration.html', context)   

# account activation view
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Account.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Thank you for your email confirmation. You can now log in to your account.')
        return redirect('login')
    else:
        messages.error(request, 'Activation link is invalid!')
        return redirect('registration')


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = auth.authenticate(request, email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'auth/login.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')
              
@login_required(login_url='login')
def dashboard(request):
    return render(request, 'dashboard.html')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)
            # reset password email
            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password'
            message = render_to_string('auth/password_reset_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            
            messages.success(request, 'Password reset email has been sent to your email address.')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist with this email address.')
            return redirect('forgot_password')
    return render(request, 'auth/forgot_password.html')

def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Account.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        return redirect('password_reset_complete')
    else:
        messages.error(request, 'The reset password link is invalid, possibly because it has already been used. Please request a new password reset.')
        return redirect('forgot_password')
    
    
    
def password_reset_complete(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password:
            uid = request.session.get('uid')
            if uid is None:
                messages.error(request, 'Session expired. Please try resetting your password again.')
                return redirect('forgot_password')
            
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            request.session.pop('uid', None) 
            messages.success(request, 'Your password has been reset successfully. You can now log in with your new password.')
            return redirect('login')
        else:
            messages.error(request, 'Passwords do not match. Please try again.')
            
            return redirect('password_reset_complete')
    
    return render(request, 'auth/password_reset_complete.html')
    
    