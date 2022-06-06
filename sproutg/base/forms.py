from dataclasses import field
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
                'type': 'text',
                'name': 'username',
                'id': 'username',
                'placeholder': 'Enter Username', 
                'class': 'required form-control',
                'autocomplete': 'off',
                'required': ''
            }
        )
        self.fields['email'].widget.attrs.update({
                'type': 'email',
                'name': 'email',
                'id': 'email',
                'placeholder': 'Enter e-mail', 
                'class': 'required form-control',
                'required': ''
            }
        )
        self.fields['password1'].widget.attrs.update({
                'type': 'password',
                'name': 'password1',
                'id': 'password1',
                'placeholder': 'Enter Password', 
                'class': 'required form-control',
                'required': ''
            }
        )
        self.fields['password2'].widget.attrs.update({
                'type': 'password',
                'name': 'password2',
                'id': 'password2',
                'placeholder': 'Confirm Password', 
                'class': 'required form-control',
                'required': ''
            }
        )
    
    class Meta:
        model = User
        fields = ['username', 'email' ,'password1', 'password2']
        
class ProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profile_pic'].widget.attrs.update({
                'type': 'file',
                'name': 'profile_pic', 
                'accept': 'image/*',
                'id': 'profile_pic_upload',
                'class': 'form-control'
            }
        )
        self.fields['full_name'].widget.attrs.update({
                'type': 'text', 
                'name': 'full_name', 
                'maxlength': '200',
                'id': 'full_name',
                'class': 'required form-control'
            }
        )
        self.fields['birth_date'].widget.attrs.update({
                'type': 'text',
                'name': 'birth_date',
                'required': '',
                'id': 'id_birth_date',
                'class': 'required form-control'
            }
        )
        self.fields['description'].widget.attrs.update({
                'name': 'description',
                'cols': '40', 
                'rows': '10',
                'id': "description"
            }
        )
       
    
    
    class Meta:
        model = Profile
        fields = ['profile_pic', 'full_name', 'birth_date', 'description']
        
    def getAllExceptPic(self):
        return [self['full_name'],self['birth_date'],self['description']]