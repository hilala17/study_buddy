from django import forms

class SignupForm(forms.Form):
    """
    Custom Signup Form for Django AllAuth
    AllAuth settings key points to this.
    """
    first_name = forms.CharField(max_length=32, label='First Name')
    last_name = forms.CharField(max_length=32, label='Last Name')

        
    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()