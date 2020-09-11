from django import forms
from localflavor.us.forms import USStateSelect

PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'Paypal')
)

IMG_SIZE_CHOICES = [
    ('5R', '5x7'),
    ('8R', '8x10'),
    ('11R', '11x14'),
    ('12S', '12x12'),
    ('16R', '16x20'),
    ('16S', '16x16'),
    ('18R', '18x24'),
    ('20R', '20x30'),
]


class CheckoutForm(forms.Form):
    shipping_first_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'First Name',
        'class': 'form-control'
    }))
    shipping_last_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Last Name',
        'class': 'form-control'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Email',
        'class': 'form-control'
    }))
    shipping_street = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Address',
        'class': 'form-control'
    }))
    shipping_apartment = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Apartment (optional)',
        'class': 'form-control'
    }))
    shipping_state = forms.CharField(widget=USStateSelect(attrs={
        'class': 'custom-select d-block w-100',
    }))
    shipping_zipcode = forms.IntegerField(widget=forms.TextInput(attrs={
        'placeholder': 'Zipcode',
        'class': 'form-control'
    }))


class ImgSizeForm(forms.Form):
    img_size = forms.ChoiceField(
        widget=forms.Select, choices=IMG_SIZE_CHOICES)
