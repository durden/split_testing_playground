from django import forms

class RegistrationForm(forms.Form):
    """Form for registering user"""

    email = forms.EmailField()
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    choice = forms.IntegerField(widget=forms.HiddenInput, required=False)
