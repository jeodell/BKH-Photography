from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={
        'placeholder': 'Name',
        'class': 'form-control mt-3'
    }))
    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={
        'placeholder': 'Email',
        'class': 'form-control mt-3'
    }))
    message = forms.CharField(label='', widget=forms.Textarea({
        'rows': 4,
        'placeholder': 'Message',
        'class': 'form-control mt-3'
    }))
