from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from pkg_resources import require

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