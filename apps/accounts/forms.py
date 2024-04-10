from django import forms
from django.contrib.auth.forms import AuthenticationForm, ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from allauth.account.forms import LoginForm, SignupForm, ResetPasswordForm

from .models import User, Address
from .validators import validate_phone_number


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="رمز عبور", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="تایید رمز عبور", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ["email", "full_name", "phone_number"]

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("رمز عبورهای وارد شده یکسان نیستند")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ["email", "phone_number", "full_name", "is_active", "is_admin"]


class AddressCreationForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ('user', 'is_active')
        widgets = {
            'address': forms.Textarea(attrs={"id": "address", "class": "form-control", 'style': 'resize:none;', 'rows': 2}),
            'phone': forms.TextInput(attrs={"id": "tel", "class": "form-control"}),
            'postal_code': forms.TextInput(attrs={"id": "postal_code", "class": "form-control"}),
            'receiver': forms.TextInput(attrs={"id": "receiver", "class": "form-control"}),
        }

    def __init__(self, user, *args, **kwargs):
        super(AddressCreationForm, self).__init__(*args, **kwargs)
        self.user = user

    def save(self, commit=True):
        # Set the user before saving
        instance = super(AddressCreationForm, self).save(commit=False)
        instance.user = self.user
        if commit:
            instance.save()
        return instance


class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['login'].widget = forms.EmailInput(
            attrs={'class': 'form-control', "autocomplete": "email", 'id': 'email'})
        self.fields['password'].widget = forms.PasswordInput(
            attrs={'class': 'form-control', "autocomplete": "password", 'id': 'password'})


class CustomSignupForm(SignupForm):
    full_name = forms.CharField(label="نام و نام خانوادگی",
                                widget=forms.TextInput(
                                    attrs={"class": "form-control", "id": "name", "autocomplete": "name"}))
    phone_number = forms.CharField(label='شماره موبایل', validators=[validate_phone_number],
                                   widget=forms.TextInput(
                                       attrs={"class": "form-control", "autocomplete": "tel"}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget = forms.EmailInput(
            attrs={'class': 'form-control', "autocomplete": "email"})
        self.fields["password1"].widget = forms.PasswordInput(
            attrs={'class': 'form-control'})
        self.fields["password2"].widget = forms.PasswordInput(
            attrs={'class': 'form-control'})


class CustomResetPasswordForm(ResetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget = forms.EmailInput(
            attrs={'class': 'form-control', "autocomplete": "email"})