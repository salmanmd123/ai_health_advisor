from django import forms
from .models import UserRegistrationModel


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = UserRegistrationModel
        fields = ['name', 'loginid', 'password', 'email', 'mobile', 'age', 'gender']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'loginid': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mobile Number'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Age'}),
            'gender': forms.Select(attrs={'class': 'form-control'},
                                   choices=[('', 'Select Gender'), ('Male', 'Male'),
                                            ('Female', 'Female'), ('Other', 'Other')]),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match!")
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.status = 'activated'
        if commit:
            instance.save()
        return instance


class SymptomInputForm(forms.Form):
    symptoms = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Describe your symptoms here (e.g., headache, fever, sore throat)...'
        }),
        label='Describe Your Symptoms'
    )
