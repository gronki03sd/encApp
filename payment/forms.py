from django import forms
from .models import ShippingAdress


class ShippingForm(forms.ModelForm):
    shipping_full_name = forms.CharField(label="" , widget=forms.TextInput(attrs={'class' : 'form-control' , 'placeholder' : 'Full Name'}), required=False)
    shipping_email = forms.CharField(label="" , widget=forms.TextInput(attrs={'class' : 'form-control' , 'placeholder' : 'Email'}), required=False)
    shipping_adress1 = forms.CharField(label="" , widget=forms.TextInput(attrs={'class' : 'form-control' , 'placeholder' : 'Adress 1'}), required=False)
    shipping_adress2 = forms.CharField(label="" , widget=forms.TextInput(attrs={'class' : 'form-control' , 'placeholder' : 'Adress 2'}), required=False)
    shipping_city = forms.CharField(label="" , widget=forms.TextInput(attrs={'class' : 'form-control' , 'placeholder' : 'City'}), required=False)
    shipping_state = forms.CharField(label="" , widget=forms.TextInput(attrs={'class' : 'form-control' , 'placeholder' : 'State'}), required=False)
    shipping_zipcode = forms.CharField(label="" , widget=forms.TextInput(attrs={'class' : 'form-control' , 'placeholder' : 'Zipcode'}), required=False)
    shipping_country = forms.CharField(label="" , widget=forms.TextInput(attrs={'class' : 'form-control' , 'placeholder' : 'Country'}), required=False)

    class Meta:
        model = ShippingAdress
        fields = ['shipping_full_name','shipping_email', 'shipping_adress1', 'shipping_adress2', 'shipping_city', 'shipping_state', 'shipping_zipcode', 'shipping_country']
        exclude = ['user',]