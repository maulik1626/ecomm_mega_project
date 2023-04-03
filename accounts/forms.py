from django import forms
from accounts.models import Account


# Create your forms here.
class  RegistrationForm(forms.ModelForm):
    
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