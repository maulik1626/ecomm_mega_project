from django import forms
from django.core.validators import RegexValidator
from accounts.models import Account


class RegistrationForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password"}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"}))
    
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'phone', 'password']
    
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs["placeholder"] = "First Name"
        self.fields["last_name"].widget.attrs["placeholder"] = "Last Name"
        self.fields["phone"].widget.attrs["placeholder"] = "Phone Number"
        self.fields["email"].widget.attrs["placeholder"] = "Email Address"
        for field in self.fields:
            self.fields[field].widget.attrs["required"] = True
            self.fields[field].widget.attrs["style"] = "color: black;"
    
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        phone = cleaned_data.get("phone")
        
        # Validate phone length
        if Account.objects.filter(phone=phone).exists():
            if len(str(phone)) != 10:
                raise forms.ValidationError(
                    "Phone number should be 10 digits."
                )
                
        # Validate password strength using a regex pattern
        # regex_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@._$])[A-Za-z\d@._$]{8,}$'
        # password_validator = RegexValidator(
        #     regex=regex_pattern,
        #     message="Password must be at least 8 characters long, with at least one uppercase letter, one number, and one of the following special characters: '@' or '.' or '_' or '$'"
        # )
        # password_validator(password)
        
        # Validate password and confirm password match
        if password != confirm_password:
            raise forms.ValidationError(
                "Password and confirm password does not match."
            )
            
        return cleaned_data
