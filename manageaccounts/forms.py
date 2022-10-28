from django.contrib.auth.forms import UserChangeForm
from django import forms
from pscmodels.models import User, Profile
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth import  get_user_model

class PasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)

class SetPasswordForm(SetPasswordForm):
    class Meta:
        model = get_user_model()
        fields = ['new_password1', 'new_password2']

class UserUpdateForm(UserChangeForm):
    password = None
    #username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'required': 'True','placeholder' : 'Username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder' : 'Email'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder' : 'First Name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder' : 'Last Name'}))
    #bio = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control', 'placeholder' : 'Bio'}))
    #profile_pic = forms.ImageField(widget=forms.FileInput(attrs={'class':'form-control'}))
    class Meta:
        model = User
        fields = ['email','first_name','last_name']

       
class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields= ['bio','profile_pic','facebook_url', 'github_url', 'twitter_url', 'website_url', 'linkedin_url']

        widgets={
            'bio': forms.Textarea(attrs={'class':'form-control', 'placeholder' : 'Bio'}),
            'profile_pic': forms.FileInput(attrs={'class':'form-control'}),
            'facebook_url': forms.TextInput(attrs={'class':'form-control','placeholder' : 'Facebook URL'}),
            'github_url': forms.TextInput(attrs={'class':'form-control','placeholder' : 'Github URL'}),
            'twitter_url' : forms.TextInput(attrs={'class':'form-control','placeholder' : 'Twitter URL'}),
            'website_url' : forms.TextInput(attrs={'class':'form-control','placeholder' : 'Website URL'}),
            'linkedin_url' :  forms.TextInput(attrs={'class':'form-control','placeholder' : 'Linkedin URL'})
        }
