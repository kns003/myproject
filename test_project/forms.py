from django import forms
import re
from test_project.forum.models import Thread, Comment
from django.contrib.auth.models import User
import logging


logger = logging.getLogger(__name__)

class ThreadForm(forms.Form):
	title = forms.CharField(max_length=30)
	description = forms.CharField(widget=forms.Textarea)

class UserRegisterForm(forms.Form):
    username = forms.CharField(max_length=30)
    first_name = forms.CharField()
    last_name = forms.CharField()
    password = forms.CharField(max_length=30,widget=forms.PasswordInput())
    re_password = forms.CharField(max_length=30,widget=forms.PasswordInput())
    email = forms.EmailField(required=False)


    def clean_password(self): 
        if 'password' in self.cleaned_data and 're_password' in self.cleaned_data:
            if self.cleaned_data['password'] != self.cleaned_data['re_password']: 
                raise forms.ValidationError("Passwords does not match.")
        return self.cleaned_data

    def clean_username(self):
        if 'username' in self.cleaned_data:
            username=self.cleaned_data['username']
            logger.debug('username:' + str(username))
            if not re.search(r'^\w+$', username):
                raise forms.ValidationError('Username can only contain letters, numbers, and the underscore characters.')
            try:
                User.objects.get(username = username)
                raise forms.ValidationError("Username '%s' is already taken. Choose different username." % username)
            except User.DoesNotExist:
                pass
        return username

    def save(self):
        new_user=User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['password'],
            self.cleaned_data['email'],
        )
        new_user.first_name=self.cleaned_data['first_name'],
        new_user.last_name=self.cleaned_data['last_name'],
        new_user.save()
    
class CommentForm(forms.Form):
    text = forms.CharField(max_length=100)
    
	

