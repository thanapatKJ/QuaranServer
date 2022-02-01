from django.forms.models import ModelForm
from django.contrib.auth.forms import UserCreationForm
from database.models import User

class UserForm(UserCreationForm):
    class Meta:
        model=User
        fields=('username','first_name','last_name','email','password','id_cards','numbers')