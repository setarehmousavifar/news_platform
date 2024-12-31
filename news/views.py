from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.views import admin_required
from .forms import NewsForm
from .models import News
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from interactions.forms import CommentForm
from interactions.models import Comment


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


# View برای لایک کردن خبر
@login_required
def like_news(request, news_id):
    news = get_object_or_404(News, id=news_id)
    if request.user in news.likes.all():
        news.likes.remove(request.user)  # اگر قبلاً لایک شده، حذف لایک
        liked = False
    else:
        news.likes.add(request.user)  # اگر لایک نشده، اضافه کن
        liked = True
    return JsonResponse({'liked': liked, 'total_likes': news.likes.count()})


# نمایش جزئیات خبر
def news_detail(request, pk):
    news = get_object_or_404(News, pk=pk)  # پیدا کردن خبر بر اساس شناسه
    comments = news.comments.all()  # گرفتن نظرات مرتبط با این خبر
    total_likes = news.likes.count()  # تعداد لایک‌ها
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.news = news
            comment.save()
            return redirect('news_detail', pk=news.pk)  # بازگشت به صفحه جزئیات خبر
    else:
        form = CommentForm()
    return render(request, 'news/news_detail.html', {'news': news, 'comments': comments, 'form': form, 'total_likes': total_likes})
