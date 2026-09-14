from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

from .models import Address


# =========================================================
# REGISTER FORM
# =========================================================

class RegisterForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Enter your password",
            }
        ),
        min_length=8
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confirm your password",
            }
        )
    )

    class Meta:

        model = User

        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
        ]

    def clean(self):

        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password:

            if password != confirm_password:

                raise forms.ValidationError(
                    "Passwords do not match."
                )

        return cleaned_data

    def save(self, commit=True):

        user = super().save(commit=False)

        user.set_password(
            self.cleaned_data["password"]
        )

        if commit:
            user.save()

        return user


# =========================================================
# CHECKOUT ADDRESS FORM
# =========================================================

class CheckoutAddressForm(forms.ModelForm):

    class Meta:

        model = Address

        fields = [
            "full_name",
            "phone",
            "address_line",
            "city",
            "state",
            "pincode",
        ]

        widgets = {

            "full_name": forms.TextInput(
                attrs={
                    "placeholder": "Enter your full name",
                    "class": "checkout-input",
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "placeholder": "Enter your phone number",
                    "class": "checkout-input",
                    "maxlength": "10",
                    "inputmode": "numeric",
                }
            ),

            "address_line": forms.Textarea(
                attrs={
                    "placeholder": "House / Door No., Street, Area",
                    "class": "checkout-input",
                    "rows": 3,
                }
            ),

            "city": forms.TextInput(
                attrs={
                    "placeholder": "Enter your city",
                    "class": "checkout-input",
                }
            ),

            "state": forms.TextInput(
                attrs={
                    "placeholder": "Enter your state",
                    "class": "checkout-input",
                }
            ),

            "pincode": forms.TextInput(
                attrs={
                    "placeholder": "Enter your pincode",
                    "class": "checkout-input",
                    "maxlength": "6",
                    "inputmode": "numeric",
                }
            ),
        }

    def clean_phone(self):

        phone = self.cleaned_data.get(
            "phone",
            ""
        ).strip()

        if not phone.isdigit():

            raise forms.ValidationError(
                "Please enter a valid phone number."
            )

        if len(phone) != 10:

            raise forms.ValidationError(
                "Phone number must contain 10 digits."
            )

        return phone


    def clean_pincode(self):

        pincode = self.cleaned_data.get(
            "pincode",
            ""
        ).strip()

        if not pincode.isdigit():

            raise forms.ValidationError(
                "Please enter a valid pincode."
            )

        if len(pincode) != 6:

            raise forms.ValidationError(
                "Pincode must contain 6 digits."
            )

        return pincode


# =========================================================
# USER LOGIN FORM
# =========================================================

class UserLoginForm(AuthenticationForm):

    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(
            attrs={
                "class": "auth-input",
                "placeholder": "Enter your username",
                "autocomplete": "off",
                "autocapitalize":"none",
                "spellcheck":"false",
                "autofocus": True,
            }
        )
    )

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "auth-input",
                "placeholder": "Enter your password",
                "autocomplete": "new-password",
            }
        )
    )