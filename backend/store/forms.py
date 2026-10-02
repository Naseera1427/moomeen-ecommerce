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
# ADD ADDRESS FORM  (My Addresses page)
# =========================================================

class AddAddressForm(forms.ModelForm):

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
                    "placeholder": "Enter full name",
                    "class": "addr-input",
                    "id": "addr-full-name",
                    "autocomplete": "name",
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "placeholder": "10-digit mobile number",
                    "class": "addr-input",
                    "id": "addr-phone",
                    "maxlength": "10",
                    "inputmode": "numeric",
                    "autocomplete": "tel",
                }
            ),

            "address_line": forms.Textarea(
                attrs={
                    "placeholder": "House / Door No., Street, Area",
                    "class": "addr-input",
                    "id": "addr-line",
                    "rows": 3,
                    "autocomplete": "street-address",
                }
            ),

            "city": forms.TextInput(
                attrs={
                    "placeholder": "City",
                    "class": "addr-input",
                    "id": "addr-city",
                    "autocomplete": "address-level2",
                }
            ),

            "state": forms.TextInput(
                attrs={
                    "placeholder": "State",
                    "class": "addr-input",
                    "id": "addr-state",
                    "autocomplete": "address-level1",
                }
            ),

            "pincode": forms.TextInput(
                attrs={
                    "placeholder": "6-digit pincode",
                    "class": "addr-input",
                    "id": "addr-pincode",
                    "maxlength": "6",
                    "inputmode": "numeric",
                    "autocomplete": "postal-code",
                }
            ),
        }

    def clean_phone(self):

        phone = self.cleaned_data.get("phone", "").strip()

        if not phone.isdigit():
            raise forms.ValidationError(
                "Please enter a valid 10-digit phone number."
            )

        if len(phone) != 10:
            raise forms.ValidationError(
                "Phone number must contain exactly 10 digits."
            )

        return phone

    def clean_pincode(self):

        pincode = self.cleaned_data.get("pincode", "").strip()

        if not pincode.isdigit():
            raise forms.ValidationError(
                "Please enter a valid pincode."
            )

        if len(pincode) != 6:
            raise forms.ValidationError(
                "Pincode must contain exactly 6 digits."
            )

        return pincode

    def clean_full_name(self):

        name = self.cleaned_data.get("full_name", "").strip()

        if len(name) < 2:
            raise forms.ValidationError(
                "Please enter a valid full name."
            )

        return name

    def clean_city(self):

        city = self.cleaned_data.get("city", "").strip()

        if len(city) < 2:
            raise forms.ValidationError(
                "Please enter a valid city name."
            )

        return city

    def clean_state(self):

        state = self.cleaned_data.get("state", "").strip()

        if len(state) < 2:
            raise forms.ValidationError(
                "Please enter a valid state name."
            )

        return state


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