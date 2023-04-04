from django.shortcuts import render, redirect
from django.contrib import messages as msgs
from django.contrib import auth
from accounts.forms import RegistrationForm
from accounts.models import Account

def register(request):
    """This function is used to register the user."""
    if request.method == 'POST':
        form = RegistrationForm(request.POST) # This is the form that is submitted by the user.
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            phone = form.cleaned_data["phone"]
            password = form.cleaned_data["password"]

            # Set username based on email and phone number
            username = email.split("@")[0]
            if Account.objects.filter(username=username).exists():
                username = username + '_' + str(phone)[-3:]
                if Account.objects.filter(username=username).exists():
                    username = username + '_' + str(phone)[-3:] + str(phone)[5:7]

            user = Account.objects.create_user(
                # first_name, last_name, username, email, phone, password
                first_name = first_name,
                last_name = last_name,
                email = email,
                phone = phone,
                username = username,
                password = password,
            )
            user.phone = phone
            user.is_active = True
            user.save()
            msgs.success(request, "Account created successfully.π")
            
            print(f"\n\n\nFirst Name: {user.first_name}")
            print(f"Email: {user.email}")
            print(f"Password: {user.password}\n\n\n")
            print(f"Password: {password}\n\n\n")
            
            return redirect("login")
    else:
        form = RegistrationForm()
    context = {
        "form": form,
    }
    return render(request, "accounts/register.html", context=context)

def login(request):
    """This function is used to login the user."""
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        
        print(f"Email: {email}")
        print(f"Password: {password}\n\n\n")
        
        user = auth.authenticate(email=email, password=password)
        
        print(f"\n\n\n User: {user}\n\n\n")
        
        if user is not None:
            auth.login(request, user)
            msgs.success(request, "You have successfully logged in.")
            return redirect("store")
        else:
            msgs.info(request, "Invalid credentials. Please try again.")
            return redirect("login")
    else:
        return render(request, "accounts/login.html")

def logout(request):
    """This function is used to logout the user."""
    return