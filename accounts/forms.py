from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from  django.contrib.auth import get_user_model 

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



class UserPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model= User
        fields = ('old_password','new_password1','new_password2' )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name,field in self.fields.items():
            field.widget.attrs['class']='form-control'
            field.help_text = ''
