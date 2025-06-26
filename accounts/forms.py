from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from  django.contrib.auth import get_user_model 
from django.contrib.auth.forms import PasswordResetForm
from django import forms 


#  usercreationfrom  le naya user create garn am help garxa 
# user creation ka lagi form banauna parxa
# sercreation le email include gardaina 


User = get_user_model()


# registraion form for creating a new user
# depending upn the need, fields haru add garna milxa 
class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name,field in self.fields.items():
            field.widget.attrs['class']='form-control'
            self.fields[field_name].help_text = ''


# password change form for changing the password of the user
class UserPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model= User
        fields = ('old_password','new_password1','new_password2' )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name,field in self.fields.items():
            field.widget.attrs['class']='form-control'
            field.help_text = ''



class CreatePasswordResetForm(PasswordResetForm):
    def clean_email(self):
        email=self.cleaned_data['email']
        user=get_user_model()
        if not user.objects.filter(email=email).exists():
            raise forms.ValidationError ("Email Address is not registered")
      

class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''