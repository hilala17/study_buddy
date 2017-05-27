
from allauth.account.forms import LoginForm, SignupForm


class MyLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        #self.fields['login'].widget = forms.TextInput(attrs={'type': 'email', 'class': 'yourclass'})
        #self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'yourclass'})
        

class MySignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        