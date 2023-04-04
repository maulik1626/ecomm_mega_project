from django.shortcuts import render, redirect
from django.contrib import messages as msgs
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
            user.save()
            msgs.success(request, "Account created successfully.π")
            return redirect("login")
    else:
        form = RegistrationForm()
    context = {
        "form": form,
    }
    return render(request, "accounts/register.html", context=context)

def login(request):
    """This function is used to login the user."""
    return render(request, "accounts/login.html")

def logout(request):
    """This function is used to logout the user."""
    return