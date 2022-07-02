from django import forms

from bookshop.models import CustomerOrder


class CustomerOrderForm(forms.ModelForm):

    class Meta:
        model = CustomerOrder
        fields = ['mail', 'city', 'post_department', 'phone_number']