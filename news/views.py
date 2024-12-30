from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.views import admin_required
from .forms import NewsForm
from .models import News

def home(request):
    return render(request, 'home.html')  # نمایش صفحه اصلی


# View برای افزودن خبر جدید
@login_required
@admin_required
def add_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('news_list')  # بازگشت به لیست اخبار
    else:
        form = NewsForm()
    return render(request, 'news/add_news.html', {'form': form})


# نمایش لیست اخبار
def news_list(request):
    news_list = News.objects.all()# گرفتن تمام اخبار از دیتابیس
    return render(request, 'news/news_list.html', {'news_list': news_list})

