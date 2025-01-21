from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import admin_required, super_admin_required
from .forms import NewsForm
from .models import News, Category
from interactions.forms import CommentForm
from interactions.models import Comment
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import NewsSerializer
from django.core.paginator import Paginator
import logging

logger = logging.getLogger(__name__)
# صفحه اصلی
def home(request):
    query = request.GET.get('q')  # گرفتن ورودی جست‌وجو از URL
    if query:
        news_list = News.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)  # جست‌وجو در عنوان و متن
        )
    else:
        news_list = News.objects.all()  # نمایش تمام اخبار در صورت نبود جست‌وجو
    
    categories = Category.objects.all()
    news_list = News.objects.filter(categories__in=categories) 

    main_categories = categories[:3]  # سه دسته اصلی
    more_categories = categories[3:]  # باقی دسته‌بندی‌ها

    logger.info(f"Latest News Count: {latest_news.count()}")
    logger.info(f"News List Count: {news_list.count()}")

    latest_news = News.objects.order_by('-published_date')[:10]  # 10 خبر اخیر
    return render(request, 'home.html', {'main_categories': main_categories, 'more_categories': more_categories, 'news_list': news_list, 'latest_news': latest_news, 'query': query})


# فقط ادمین‌ها و سوپریوزرها اجازه دارند به این ویو دسترسی پیدا کنند
def admin_required(user):
    return user.user_type in ['admin', 'super_admin']

@login_required
@user_passes_test(admin_required)
def create_news(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        category_ids = request.POST.getlist('categories')  # دریافت لیست ID دسته‌بندی‌ها
        image = request.FILES.get('image')

        # ایجاد خبر
        news = News.objects.create(
            title=title,
            content=content,
            author=request.user,
            image=image
        )

        # اضافه کردن دسته‌بندی‌ها به خبر
        if category_ids:
            categories = Category.objects.filter(id__in=category_ids)
            news.categories.set(categories)

        news.save()
        return redirect('news_list')

    categories = Category.objects.all()  # گرفتن لیست دسته‌بندی‌ها
    return render(request, 'news/create_news.html', {'categories': categories})


@login_required
@user_passes_test(admin_required)
def edit_news(request, pk):
    news = get_object_or_404(News, pk=pk)
    if request.user.is_superuser or request.user == news.author:
        if request.method == 'POST':
            form = NewsForm(request.POST, request.FILES, instance=news)
            if form.is_valid():
                form.save()
                return redirect('news_detail', pk=news.pk)
        else:
            form = NewsForm(instance=news)
        return render(request, 'news/edit_news.html', {'form': form, 'news': news})
    else:
        return redirect('news_list')  # اگر دسترسی نداشت، هدایت به صفحه اصلی

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
    category_id = request.GET.get('category')
    sort = request.GET.get('sort')
    if query:
        news_list = News.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)  # جست‌وجو در عنوان و متن
        )
    if category_id:
        news_list = news_list.filter(categories__id=category_id)

    if sort == 'latest':
        news_list = news_list.order_by('-published_date')
    elif sort == 'popular':
        news_list = news_list.order_by('-views_count')
        
    else:
        news_list = News.objects.all()  # نمایش تمام اخبار در صورت نبود جست‌وجو

    # صفحه‌بندی
    paginator = Paginator(news_list, 6)  # نمایش 6 خبر در هر صفحه
    page = request.GET.get('page')
    news = paginator.get_page(page)

    categories = Category.objects.all()

    latest_news = News.objects.order_by('-published_date')[:10]  # 10 خبر اخیر

    return render(request, 'news/news_list.html', {'news_list': news_list, 'categories': categories, 'latest_news': latest_news, 'query': query})


# نمایش جزئیات خبر
def news_detail(request, pk):
    news = get_object_or_404(News, pk=pk)  # پیدا کردن خبر بر اساس شناسه
    total_likes = news.liked_by.count()  # تعداد لایک‌ها
    related_news = News.objects.filter(categories__in=news.categories.all()).exclude(id=news.id)[:5]  # 5 خبر مرتبط
    news.views_count += 1
    news.save()
    comments = Comment.objects.filter(news=news, parent=None)  # نظرات اصلی
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
    return render(request, 'news/news_detail.html', {'news': news, 'total_likes': total_likes, 'related_news': related_news, 'comments': comments, 'form': form})


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


def category_news(request, category_name):
    news_list = News.objects.filter(categories__name__iexact=category_name)
    return render(request, 'news/category_news.html', {'news_list': news_list, 'category_name': category_name})
