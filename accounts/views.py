from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from contacts.models import Contact
from re import search

def register(request):
    if request.method == 'POST':
        # Get Form Values:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # Check if Passwords match:
        if password == password2:
            # Check password requirement:
            if ((len(password) >= 8) and (search('[0-9]', password) is not None) and (search('[A-Z]', password) is not None)):
                # Check if username exist:
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'This Username already taken!')
                    return redirect('accounts:register')
                else:
                    # Check if email exist:
                    if User.objects.filter(email=email).exists():
                        messages.error(request, 'This Email is registered!')
                        return redirect('accounts:register')
                    else:
                        # Ready to Register:
                        user = User.objects.create_user(
                            first_name=first_name,
                            last_name=last_name,
                            username=username,
                            email=email,
                            password=password
                        )
                        user.save()
                        ### Login Automatically after Register:
                        ### auth.login(request, user)
                        ### messages.success(request, 'Welcome ' + username)
                        ### return redirect('accounts:dashboard')
                        messages.success(request, 'Your account is registred successfuly, you can login now')
                        return redirect('accounts:login')
            else:
                messages.error(request, 'Poor Password! the length should be greater than 8 characters, include Uppercases and numerical')
                return redirect('accounts:register')
        else:
            messages.error(request, 'Passwords not match!')
            return redirect('accounts:register')
    return render(request, 'accounts/register.html')

def login(request):
    if request.method == 'POST':
        # Get user Infos:
        username = request.POST['username']
        password = request.POST['password']
        # Check if the Username
        if User.objects.filter(username=username).exists():
            # Authenticate:
            user = auth.authenticate(
                username=username,
                password=password
            )
            if user is not None:
                auth.login(request, user)
                messages.success(request, 'Logged Successfuly')
                return redirect('accounts:dashboard')
            else:
                messages.error(request, 'Invalid Password!')
                return redirect('accounts:login')
        else:
            messages.error(request, 'Invalid Username!')
            return redirect('accounts:login')
    return render(request, 'accounts/login.html')

def forgetPassword(request):
    return render(request, 'accounts/forgetPassword.html')

def dashboard(request):
    user_contacts = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)
    context = {
        'contacts': user_contacts
    }
    return render(request, 'accounts/dashboard.html', context)

def logout(request):
    if request.method == 'POST':
        messages.success(request, 'See you soon ' + request.user.username)
        auth.logout(request)
        return redirect('pages:index')