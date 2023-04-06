from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages as msgs
from django.contrib import auth
from accounts.forms import RegistrationForm
from accounts.models import Account
from django.contrib.auth.hashers import check_password
from carts.views import _cart_id
from carts.models import Cart, CartItem

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
            current_site = get_current_site(request)    # get current site domain name
            mail_subject = 'Activate your account.'     # email subject
            message = render_to_string(                 # email message
                'accounts/acc_active_email.html',       # email template
                {
                "user": user, 
                "domain": current_site.domain, 
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),     # encode user id
                "token": default_token_generator.make_token(user),      # generate token
                }                                       # email template context
            )
            to_email = email                            # email receiver
            send_email = EmailMessage(mail_subject, message, to=[to_email])  # email sender
            send_email.send()                           # send email
            
            context={"email": email}
             
            return redirect(f'/accounts/login/?command=verification&email={email}&is_active={user.is_active}_verification_pending_{urlsafe_base64_encode(force_bytes(user.pk))}')       # redirect to login page
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
        try:
            user = Account.objects.get(email=email)
            if user.is_active == False:
                return redirect(f"/accounts/login/?command=verification&email={email}&is_active={user.is_active}_verification_pending_{urlsafe_base64_encode(force_bytes(user.pk))}")
            else:
                user = auth.authenticate(email=email, password=password)
                if user is not None:
                    try:
                        cart = Cart.objects.get(cart_id=_cart_id(request))
                        cart_items_extsts = CartItem.objects.filter(cart=cart).exists()
                        if cart_items_extsts:
                            cart_items = CartItem.objects.filter(cart=cart)
                            for i in cart_items:
                                i.user = user
                                i.save()
                    except:
                        pass
                    auth.login(request, user)
                    msgs.success(request, "You have successfully logged in.")
                    return redirect("store")
                else:
                    msgs.info(request, "Invalid credentials. Please try again.")
                    return redirect(f"/accounts/login/?command=invalid_credentials&email={email}")
        except Account.DoesNotExist:
            msgs.info(request, "Register your account first.")
            return redirect(f"/accounts/register/?command=user_not_found&email={email}")
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
        uid = urlsafe_base64_decode(uidb64).decode()        # decode user id
        user = Account._default_manager.get(pk=uid)         # get user based on user id after decoding
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        msgs.success(request, "Thank you for your email confirmation. Now you can login your account.")
        return redirect(login)
    else:
        msgs.info(request, "Activation link is invalid!")
        return redirect("register")

@login_required(login_url="login")
def dashboard(request):
    """This function is used to show the user dashboard."""
    return render(request, "accounts/dashboard.html")

def forgot_password(request):
    """This function is used to send the forgot password link to the user."""
    if request.method == "POST":
        email = request.POST["email"]
        
        # check is the email is registered in the database or not
        if Account.objects.filter(email=email).exists():
            # reset user password using email verification
            user = Account.objects.get(email__iexact=email)
            
            current_site = get_current_site(request)    # get current site domain name
            mail_subject = 'Reset your password.'       # email subject
            message = render_to_string(
                'accounts/password_reset_email.html',   # email template
                {
                    'user' : user,                                           # user
                    'domain' : current_site.domain,                          # domain name
                    'uid' : urlsafe_base64_encode(force_bytes(user.pk)),     # encode user id
                    'token' : default_token_generator.make_token(user),      # generate token
                }
            )
            to_mail = email
            send_email = EmailMessage(mail_subject, message, to=[to_mail])   # email sender
            send_email.send()                           # send email

            return redirect(f"/accounts/login/?command=password_reset_link_sent&email={email}&is_active={user.is_active}_verification_pending_{urlsafe_base64_encode(force_bytes(user.pk))}")       # redirect to login page
        else:
            msgs.error(request, f"'{email}' is not registered.")
            return redirect("forgot_password")
    else:
        return render(request, "accounts/forgot_password.html")

def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        context = {'email' : user.email}
        return render(request, "accounts/reset_password.html", context)
    else:
        msgs.info(request, "This link has been expired!")
        return redirect("login")

def reset_password(request):    
    try:
        # get user from session
        uid = request.session.get('uid')
        user = Account.objects.get(pk=uid)
        
        if request.method == "POST":
            
            # get password and confirm password from form
            password = request.POST["password"]
            confirm_password = request.POST["confirm_password"]
            email = request.POST["email"]
            
            # check is the password from the from is the same as user.password
            if check_password(password, user.password):
                msgs.error(request, "New password cannot be the same as old password.")
                context = {'email' : email}
                return render(request, "accounts/reset_password.html", context)
            else:
                if password == "":
                    msgs.error(request, "Password cannot be empty.")
                    context = {'email' : email}
                    return render(request, "accounts/reset_password.html", context)
                elif password == confirm_password:
                    user.set_password(password)
                    user.save()
                    msgs.success(request, "Password reset successful.")
                    return redirect("login")
                else:
                    msgs.error(request, "New Password and Confirm New Password does not match.")
                    context = {'email' : email}
                    return render(request, "accounts/reset_password.html", context)
        
        return render(request, "accounts/reset_password.html")

    except:
        msgs.info(request, "This link has been expired!")
        return redirect("login")