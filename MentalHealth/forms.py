from django import forms
from .models import Checkout, Images, Professional


class ProfessionalForm(forms.ModelForm):
    class Meta:
        model = Professional
        fields = ['name', 'specialization', 'description', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'specialization': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Checkout
        fields = ['name', 'email', 'phone', 'payment_method']
        widgets = {
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = ['image', 'title', 'price']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
