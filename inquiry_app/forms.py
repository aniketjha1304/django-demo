from django import forms
from .models import InquiryForm
import re


class InquiryFormForm(forms.ModelForm):
    class Meta:
        model = InquiryForm
        fields = [
            "first_name",
            "last_name",
            "phone",
            "email",
            "gender",
            "marital_status",
        ]
        widgets = {
            "first_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter first name"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter last name"}
            ),
            "phone": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter phone number"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Enter email address"}
            ),
            "gender": forms.RadioSelect(),
            "marital_status": forms.RadioSelect(),
        }

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        # Check if first name contains only alphabets
        if not re.match("^[A-Za-z ]+$", first_name):
            raise forms.ValidationError("First name should contain only characters.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name")
        # Check if last name contains only alphabets
        if not re.match("^[A-Za-z ]+$", last_name):
            raise forms.ValidationError("Last name should contain only characters.")
        return last_name

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        # Check if phone contains only numbers
        if not re.match("^[0-9]+$", phone):
            raise forms.ValidationError("Phone number should contain only numbers.")
        if len(phone) < 10:
            raise forms.ValidationError("Phone number should be at least 10 digits.")
        return phone
