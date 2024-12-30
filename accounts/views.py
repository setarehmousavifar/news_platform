from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm

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
