from django.shortcuts import render, redirect
from accounts.forms import RegistrationForm
from accounts.models import Account

def register(request):
    """This function is used to register the user."""
    print("\n\nEnter Register Function\n\n")

    if request.method == 'POST':
        
        print("\n\nEnter IF Block\n\n")
        
        form = RegistrationForm(request.POST) # This is the form that is submitted by the user.
        print("\n\nForm Received\n\n")
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            phone = form.cleaned_data["phone"]
            password = form.cleaned_data["password"]

            print("\n\nForm Validated\n\n")
            
            user = Account.objects.create_user(
                # first_name, last_name, username, email, phone, password
                first_name = first_name,
                last_name = last_name,
                email = email,
                phone = phone,
                username = email.split("@")[0],
                password = password,
            )
            print("\n\n\nUser saved successfully.\n\n\n")
            
            return redirect("login")
    else:
        
        print("\n\nEnter Else Block\n\n")
        
        form = RegistrationForm()


    context = {
        "form": form,
    }
    
    print("\n\nEnd Function\n\n")
    
    return render(request, "accounts/register.html", context=context)

def login(request):
    """This function is used to login the user."""
    return render(request, "accounts/login.html")

def logout(request):
    """This function is used to logout the user."""
    return