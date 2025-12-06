from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import User


class CustomLoginForm(AuthenticationForm):
    role = forms.ChoiceField(
        choices=User.Roles.choices, 
        label="Role",
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'placeholder': 'Select your role'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your username'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your password'
        })
        self.fields['role'].widget.attrs.update({
            'class': 'form-select',
            'placeholder': 'Select your role'
        })


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")
    role = forms.ChoiceField(choices=User.Roles.choices, label="Role")
    reg_no = forms.CharField(required=False, label="Registration Number")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "role", "reg_no")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Simplify username help text and placeholders
        self.fields["username"].help_text = "Use letters, digits, or @/./+/-/_ (no spaces)."
        self.fields["username"].label = "Username"
        self.fields["username"].widget.attrs.update({"placeholder": "e.g., 21CS001 or john_doe"})
        self.fields["email"].widget.attrs.update({"placeholder": "name@example.com"})
        self.fields["reg_no"].widget.attrs.update({"placeholder": "Optional (students)"})

    def clean_username(self):
        username = self.cleaned_data.get("username", "")
        if not username:
            raise ValidationError("Username is required.")
        sanitized = username.strip().lower().replace(" ", "_")
        return sanitized


class UserUpdateForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "role", "reg_no")

