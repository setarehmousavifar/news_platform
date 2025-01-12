from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import admin_required, super_admin_required
from .forms import NewsForm
from .models import News
from django.http import JsonResponse
from interactions.forms import CommentForm
from interactions.models import Comment
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import NewsSerializer

# صفحه اصلی
def home(request):
    query = request.GET.get('q')  # گرفتن ورودی جست‌وجو از URL
    if query:
        news_list = News.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)  # جست‌وجو در عنوان و متن
        )
    else:
        news_list = News.objects.all()  # نمایش تمام اخبار در صورت نبود جست‌وجو
    
    latest_news = News.objects.order_by('-published_date')[:10]  # 10 خبر اخیر
    return render(request, 'home.html', {'news_list': news_list, 'latest_news': latest_news, 'query': query})


# فقط ادمین‌ها و سوپریوزرها اجازه دارند به این ویو دسترسی پیدا کنند
def admin_required(user):
    return user.user_type in ['admin', 'super_admin']

@login_required
@user_passes_test(admin_required)
def create_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.save()
            return redirect('news_list')  # بعد از ثبت خبر به لیست اخبار برگردد
    else:
        form = NewsForm()
    return render(request, 'news/create_news.html', {'form': form})

@login_required
@user_passes_test(admin_required)
def edit_news(request, pk):
    news = get_object_or_404(News, pk=pk)
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES, instance=news)
        if form.is_valid():
            form.save()
            return redirect('news_list')
    else:
        form = NewsForm(instance=news)
    return render(request, 'news/edit_news.html', {'form': form})

@login_required
@user_passes_test(admin_required)
def delete_news(request, pk):
    news = get_object_or_404(News, pk=pk)
    if request.method == 'POST':
        news.delete()
        return redirect('news_list')
    return render(request, 'news/delete_news.html', {'news': news})


# نمایش لیست اخبار
def news_list(request):
    query = request.GET.get('q')  # گرفتن ورودی جست‌وجو از URL
    if query:
        news_list = News.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)  # جست‌وجو در عنوان و متن
        )
    else:
        news_list = News.objects.all()  # نمایش تمام اخبار در صورت نبود جست‌وجو

    if request.user.user_type == 'admin':
        news_list = News.objects.filter(author=request.user)

    latest_news = News.objects.order_by('-published_date')[:10]  # 10 خبر اخیر
    return render(request, 'news/news_list.html', {'news_list': news_list, 'latest_news': latest_news, 'query': query})


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
    related_news = News.objects.filter(category=news.category).exclude(id=news.id)[:5]  # 5 خبر مرتبط
    news.views_count += 1
    news.save()
    comments = Comment.objects.filter(news=news, parent=None)  # نظرات اصلی
    total_likes = news.likes.count()  # تعداد لایک‌ها
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            parent_id = request.POST.get("parent_id")  # گرفتن ID والد
            parent = Comment.objects.get(id=parent_id) if parent_id else None
            comment = form.save(commit=False)
            comment.user = request.user
            comment.news = news
            comment.parent = parent  # تنظیم والد
            comment.save()
            return redirect('news_detail', pk=news.pk)  # بازگشت به صفحه جزئیات خبر
    else:
        form = CommentForm()
    return render(request, 'news/news_detail.html', {'news': news, 'related_news': related_news, 'comments': comments, 'form': form, 'total_likes': total_likes})


@api_view(['GET'])
def news_list_api(request):
    news = News.objects.all()
    serializer = NewsSerializer(news, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def news_detail_api(request, pk):
    news = News.objects.get(pk=pk)
    serializer = NewsSerializer(news)
    return Response(serializer.data)
