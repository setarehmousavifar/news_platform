from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import user_passes_test, login_required
from django.http import HttpResponseForbidden  # برای پاسخ مناسب در دسترسی غیرمجاز
from .models import SiteSettings
from django.contrib import messages
from .forms import UserProfileForm


# نمایش و مدیریت فرم ثبت‌نام
def register(request):
    """
    ویوی ثبت‌نام کاربران جدید
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # ذخیره کاربر جدید
            login(request, user)  # ورود خودکار پس از ثبت‌نام
            next_url = request.GET.get('next')  # بررسی وجود مسیر مورد نظر
            if next_url:
                return redirect(next_url)  # هدایت به مسیر مورد نظر
            return redirect('home')  # هدایت به صفحه اصلی اگر مسیر خاصی وجود نداشت
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


# ورود کاربران
def user_login(request):
    """
    ویوی ورود کاربران به سیستم
    """
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next')  # بررسی وجود مسیر مورد نظر
                if next_url:
                    return redirect(next_url)  # هدایت به مسیر مورد نظر
                return redirect('home')  # هدایت به صفحه اصلی اگر مسیر خاصی وجود نداشت
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


# خروج کاربران
def user_logout(request):
    """
    ویوی خروج کاربران
    """
    logout(request)
    return redirect('home')  # بازگشت به صفحه اصلی پس از خروج


@login_required
def profile_view(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserProfileForm(instance=user)

    return render(request, 'accounts/profile.html', {'form': form})


# بررسی نقش ادمین
def is_admin(user):
    """
    بررسی می‌کند که آیا کاربر ادمین یا کاربر ارشد است.
    """
    return user.user_type == 'admin' or user.user_type == 'super_admin'


# Decorator برای دسترسی فقط ادمین‌ها
admin_required = user_passes_test(is_admin)


# مدیریت برای ادمین‌ها
@admin_required
@login_required
def admin_dashboard(request):
    """
    ویوی مخصوص ادمین برای مدیریت بخش‌ها
    """
    if request.user.user_type not in ['admin', 'super_admin']:
        # اگر کاربر دسترسی لازم را نداشته باشد
        return HttpResponseForbidden("شما اجازه دسترسی به این بخش را ندارید.")
    
    # نمایش داشبورد ادمین
    return render(request, 'accounts/admin_dashboard.html')


def home_view(request):
    settings = SiteSettings.objects.first()  # دریافت اولین تنظیمات سایت
    return render(request, 'home.html', {'settings': settings})