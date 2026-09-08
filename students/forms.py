from django import forms
from .models import Student

class StudentForm(forms.Form):
    firstname = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter firstname"
            }
        )
    )
    surname = forms.CharField(max_length=100)
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data["email"]

        if not email.endswith("@university.edu"):
            raise forms.ValidationError(
                "Students must use a university email"
            )
        return email 

    def clean(self):
        cleaned_data = super().clean()

        firstname = cleaned_data.get("firstname")
        email = cleaned_data.get("email")

        if firstname and email:
            email_username = email.split("@")[0]

            if email_username.lower() != firstname.lower():
                raise forms.ValidationError(
                    "The Email username must match the firstname"
                )
        return cleaned_data


class StudentModelForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            "firstname",
            "surname",
            "email",
            "date_of_birth",
            "department",
            "profile_picture",
        ]

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if email and not email.endswith("@university.edu"):
            raise forms.ValidationError(
                "Students must use university mail"
            )
        return email
