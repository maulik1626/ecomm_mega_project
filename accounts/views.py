from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages as msgs
from django.contrib import auth
from accounts.forms import RegistrationForm
from accounts.models import Account
# from django.contrib.auth.decorators import user_passes_test

# verify email
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string 
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


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
            
            
            # USER Activation
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string(
                'accounts/acc_active_email.html', 
                {
                "user": user, 
                "domain": current_site.domain, 
                "uid": urlsafe_base64_encode(force_bytes(user.pk)), 
                "token": default_token_generator.make_token(user),
                }
            )
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            
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

@login_required(login_url="login")
def logout(request):
    """This function is used to logout the user."""
    auth.logout(request)
    msgs.success(request, "You have successfully logged out.")
    return redirect("login")


def activate(request, uidb64, token):
    """This function is used to activate the user."""
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        msgs.success(request, "Thank you for your email confirmation. Now you can login your account.")
        return redirect("login")
    else:
        print("\n\n\nActivation link is invalid!\n\n\n")
        msgs.info(request, "Activation link is invalid!")
        return redirect("register")