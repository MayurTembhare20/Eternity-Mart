from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django import forms
from django.contrib.auth.models import User
from user_profile.models import User_Profile

class UserAuthenticationForm(AuthenticationForm):
    """ Extending Django's AuthenticationForm form to add form-control class """
    next_url = forms.CharField(widget= forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        super(UserAuthenticationForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserRegistrationForm(UserCreationForm):
    """ Extending Django's UserCreation form to add form-control class """

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            
class UserForm(forms.ModelForm):
    """ Form to update User's basic information """

    class Meta:
        model = User
        fields = ['first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class UserProfileForm(forms.ModelForm):
    """ Form to update user's additional information """

    class Meta:
        model = User_Profile
        fields = ['mobile', 'address']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


