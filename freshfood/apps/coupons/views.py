from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic import FormView

from .models import Coupon
from .forms import CouponApplyForm


class CouponApplyView(FormView):
    def post(self, request):
        now = timezone.now()
        form = CouponApplyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                coupon = Coupon.objects.get(code__iexact=code,
                                            valid_from__lte=now,
                                            valid_to__gte=now,
                                            active=True)
                request.session['coupon_id'] = coupon.id
            except Coupon.DoesNotExist:
                request.session['coupon_id'] = None
        return redirect('cart:cart_detail')
