from django import forms
from django.utils.translation import gettext_lazy as _


class CouponApplyForm(forms.Form):
    code = forms.CharField(label='', widget=forms.TextInput(
        attrs={'placeholder': _('Enter coupon code')}))
