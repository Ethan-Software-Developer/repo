from django import forms
from .models import CustomUser, Profile

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=8)
    confirm_password = forms.CharField(widget=forms.PasswordInput, min_length=8)

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data



class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


    class Meta:
        model = CustomUser
        fields = [ "email", "first_name", "last_name"]

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture']

        widgets = {
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'})
        }
        
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["email", "first_name", "last_name"]

