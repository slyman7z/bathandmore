from django.shortcuts import redirect, render
from .forms import RegistrationForm
from .models import Account

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
    else:
        form = RegistrationForm()
       
    context = {
        'form': form
    }
    return render(request, 'registration.html', context)

def login(request):
    return render(request, 'login.html')
