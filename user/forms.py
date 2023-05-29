from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'palceholder': 'Email'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            field = self.fields[field_name]
            field.widget.attrs['class'] = 'form-control mt-2'

    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if CustomUser.objects.filter(email=email).first():
            raise forms.ValidationError(f"Email {email} já está em uso")
        return email


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email',)


class CustomUserLoginForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    email = forms.EmailField(widget=forms.EmailInput, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            field = self.fields[field_name]
            field.widget.attrs['class'] = 'form-control mt-2'


class UserFormChange(forms.ModelForm):

    birthday = forms.DateTimeInput()

    class Meta:
        model = CustomUser
        fields = ('name', 'profile_image', 'birthday')
