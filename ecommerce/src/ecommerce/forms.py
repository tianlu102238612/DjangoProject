from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

    
class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'class':'form-control','placeholder':'enter your name'}))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class':'form-control','placeholder':'enter your password'}))    

class RegisterForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'class':'form-control','placeholder':'enter your name'}))
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={'class':'form-control','placeholder':'enter your email'}))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class':'form-control','placeholder':'enter your password'}))   
    cpassword = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class':'form-control','placeholder':'confirm your password'}),
        label = 'confirm password')   
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError("username alreay taken")
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("the email alreay registered")
        return email
    
    def clean(self):
        data = self.cleaned_data
        password = self.cleaned_data.get('password')
        cpassword = self.cleaned_data.get('cpassword')
        
        if cpassword != password:
            raise forms.ValidationError("Passwords must be the same")
        return data
        
