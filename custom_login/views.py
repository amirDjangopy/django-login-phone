from django.shortcuts import render
from django.contrib.auth import login
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import MyUser
from . import forms
from . import helper
from django.contrib import messages

# Create your views here.

def register_view(request):
    form = forms.RegisterForm
    messages.success(request, "Test erors messages")
    if request.method == "POST":
        try:
            if "mobile" in request.POST:
                mobile = request.POST.get('mobile')
                user = MyUser.objects.get(mobile=mobile)
                # send otp
                otp = helper.get_random_otp()
                # helper.send_otp(mobile, otp)
                # helper.send_otp(mobile, otp)
                # save otp
                print(otp)
                user.otp = otp
                user.save()
                request.session['user_mobile'] = user.mobile
                return HttpResponseRedirect(reverse('custom_login:verify'))

        except MyUser.DoesNotExist:
            form = forms.RegisterForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                # send otp
                otp = helper.get_random_otp()
                # helper.send_otp(mobile, otp)
                # helper.send_otp_soap(mobile, otp)
                # save otp
                print(otp)
                user.otp = otp
                user.is_active = False
                user.save()
                request.session['user_mobile'] = user.mobile
                return HttpResponseRedirect(reverse('custom_login:verify'))
    return render(request, 'custom_login/register.html', {'form': form})




def verify(request):
    try:
        mobile = request.session.get('user_mobile')
        user = MyUser.objects.get(mobile = mobile)

        if request.method == "POST":

            # check otp expiration
            if not helper.check_otp_expiration(user.mobile):
                messages.danger(request, "OTP is expired, please try again.")
                return HttpResponseRedirect(reverse('custom_login:register_view'))

            if user.otp != int(request.POST.get('otp')):
                messages.error(request, "OTP is incorrect.")
                return HttpResponseRedirect(reverse('custom_login:verify'))

            user.is_active = True
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse('custom_login:dashboard'))

        return render(request, 'custom_login/verify.html', {'mobile': mobile})

    except MyUser.DoesNotExist:
        messages.error(request, "Error accorded, try again.")
        return HttpResponseRedirect(reverse('custom_login:register_view'))


# def mobile_login(request):
#     if request.method == "POST":
#         if "mobile" in request.POST:
#             mobile = request.POST.get('mobile')
#             user = MyUser.objects.get(mobile=mobile)
#             login(request, user)
#             return HttpResponseRedirect(reverse('dashboard'))

#     return render(request, 'custom_login/mobile_login.html')

def dashboard(request):
    return render(request, 'custom_login/dashboard.html')
