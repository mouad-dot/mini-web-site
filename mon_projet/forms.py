from django import forms
from .models import student, Employee,Person

class LoginForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control email-input'})
    )
    password = forms.CharField(
        label='Mot de passe',
        widget=forms.PasswordInput(attrs={'class': 'form-control password-input'})
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        if email and password:
            result = Person.objects.filter(password=password, email=email).exists()
            if not result:
                raise forms.ValidationError("Adresse ou mot de passe incorrects.")
        return cleaned_data

class StudentProfilForm(forms.ModelForm):
    class Meta:
        model = student
        fields = ['first_name', 'last_name', 'birth_date', 'email', 'tlfn', 'password', 'Faculte', 'annee', 'cursus']

class EmployeeProfilForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'birth_date', 'email', 'tlfn', 'password', 'Faculte', 'office', 'campus', 'job']