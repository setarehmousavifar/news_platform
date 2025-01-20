from django.shortcuts import render, get_object_or_404, redirect
from .models import Comment
from .forms import CommentForm
from news.models import News 
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Like

@login_required
def add_comment(request, pk):
    news = get_object_or_404(News, pk=pk) # گرفتن خبر مورد نظر

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)  # ایجاد شیء نظر بدون ذخیره در دیتابیس
            comment.news = news  # تنظیم خبر مرتبط با نظر
            comment.user = request.user  # تنظیم کاربر ارسال‌کننده نظر
            comment.save()  # ذخیره نظر در دیتابیس
            return redirect('news_detail', pk=pk)  # بازگشت به صفحه جزئیات خبر
    else:
        # مقداردهی اولیه parent برای ریپلای
        parent_id = request.GET.get('parent', None)
        form = CommentForm(initial={'parent': parent_id})

    return render(request, 'interactions/add_comment.html', {'form': form, 'news': news})


@login_required
def like_news(request, news_id):
    news = get_object_or_404(News, id=news_id)
    like, created = Like.objects.get_or_create(user=request.user, news=news)

    if not created:
        like.delete()
        liked = False
    else:
        liked = True

    return JsonResponse({
        "liked": liked,
        "total_likes": news.total_likes(),
    })
