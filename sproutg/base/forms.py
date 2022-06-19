from pyexpat import model
from .models import Game, Profile, Review, Developer
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django import forms

class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Username:'
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
        self.fields['email'].label = 'E-mail:'
        self.fields['email'].widget.attrs.update({
                'type': 'email',
                'name': 'email',
                'id': 'email',
                'placeholder': 'Enter e-mail', 
                'class': 'required form-control',
                'required': ''
            }
        )
        self.fields['password1'].label = 'Password:'
        self.fields['password1'].widget.attrs.update({
                'type': 'password',
                'name': 'password1',
                'id': 'password1',
                'placeholder': 'Enter Password', 
                'class': 'required form-control',
                'required': ''
            }
        )
        self.fields['password2'].label = 'Confirm Password:' 
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
                'id': 'profile_pic',
                'class': 'note-image-input note-form-control note-input'
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
        self.fields['birth_date'].label = 'Birthday'
        self.fields['birth_date'].widget.attrs.update({
                'type': 'text',
                'name': 'birth_date',
                'required': '',
                'id': 'id_birth_date',
                'class': 'required form-control'
            }
        )
        self.fields['description'].label = 'About Me'
        self.fields['description'].widget.attrs.update({
                'name': 'description',
                'cols': '40', 
                'rows': '6',
                'id': 'description',
                'class': 'form-control'
            }
        )
    
    class Meta:
        model = Profile
        fields = ['profile_pic', 'full_name', 'birth_date', 'description']
        
    def getAllExceptPic(self):
        print(self.fields['profile_pic'])
        return [self['full_name'],self['birth_date'],self['description']]


class ReviewForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['title'].widget.attrs.update({
                'type': 'text', 
                'name': 'full_name', 
                'maxlength': '200',
                'class': 'required form-control',
                'placeholder': 'Review Title',
                'autocomplete': 'off'
            }
        )
        self.fields['body'].widget.attrs.update({
                'name': 'description',
                'cols': '40', 
                'rows': '6',
                'class': 'required form-control',
                'placeholder': 'Leave a Review',
                'autocomplete': 'off'
            }   
        )
        
    class Meta:
        model = Review
        fields = ['title', 'body']


class GameForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['name'].widget.attrs.update({
                'type': 'text', 
                'name': 'name', 
                'maxlength': '200',
                'id': 'name',
                'class': 'required form-control'
            }
        )
        self.fields['publisher'].widget.attrs.update({
                'type': 'text', 
                'name': 'publisher', 
                'maxlength': '200',
                'id': 'publisher',
                'class': 'required form-control'
            }
        )
        self.fields['price'].widget.attrs.update({
                'type': 'text', 
                'name': 'price', 
                'id': 'price',
                'class': 'required form-control'
            }
        )
        self.fields['description'].widget.attrs.update({
                'type': 'textaewa', 
                'name': 'description', 
                'maxlength': '200',
                'id': 'description',
                'class': 'form-control',
                'col': '4'
            }
        )
        
    class Meta:
        model = Game
        fields = ['name', 'genres', 'publisher', 'price','description']
        