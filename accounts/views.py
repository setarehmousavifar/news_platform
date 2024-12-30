from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import user_passes_test

# نمایش و مدیریت فرم ثبت‌نام
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # ذخیره کاربر جدید
            login(request, user)  # ورود خودکار پس از ثبت‌نام
            return redirect('home')  # بازگشت به صفحه اصلی
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


# View ورود کاربران
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # هدایت به صفحه اصلی پس از ورود
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


# View خروج کاربران
def user_logout(request):
    logout(request)
    return redirect('home')  # بازگشت به صفحه اصلی پس از خروج


# بررسی نقش ادمین
def is_admin(user):
    return user.is_admin or user.is_superuser

# Decorator برای دسترسی فقط ادمین‌ها
admin_required = user_passes_test(is_admin)


