from django import forms
from django.contrib.auth.models import User


class SearchForm(forms.Form):
    search = forms.CharField(max_length=250, widget=forms.TextInput(attrs={'class': 'form-control mr-sm-2', 'placeholder': 'Look for a shop...', 'aria-label': 'Look for a shop...'}))


class LoginForm(forms.ModelForm):
    email = forms.EmailField(max_length=250, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email', 'aria-label': 'Enter email'}))
    password = forms.CharField(max_length=250, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'aria-label': 'Password'}))
    class Meta:
        model = User
        fields = ['email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        user = User.objects.filter(email=email)
        if user.exists():
            user = user.first()
            if not user.check_password(password):
                self.add_error('password', 'Invalid password!')
        else:
            self.add_error('email', 'Invalid email')

class SignUpForm(forms.ModelForm):
    email = forms.EmailField(max_length=250, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email', 'aria-label': 'Enter email'}))
    password = forms.CharField(max_length=250, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'aria-label': 'Password'}))
    password_confirmation = forms.CharField(max_length=250, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password', 'aria-label': 'Password'}))

    class Meta:
        model = User
        fields = ['email', 'password', 'password_confirmation']

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        password_confirmation = cleaned_data.get('password_confirmation')
        if password != password_confirmation:
            self.add_error('password_confirmation', 'Unconfirmed password!')
        elif len(password) <= 4:
            self.add_error('password', 'Weak password!(more than 5 letters)')
        elif User.objects.filter(email=email).exists():
            self.add_error('email', 'Email already used')



