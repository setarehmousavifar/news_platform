from django.db import models
from accounts.models import CustomUser
from news.models import News

# Comment Model
class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="comments", verbose_name="User")
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name="comments", verbose_name="News")
    content = models.TextField(verbose_name="Comment Content")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies', verbose_name="Parent Comment")

    def __str__(self): return f"{self.user.username} - {self.news.title}"

# Like Model
class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="likes", verbose_name="User")
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name="liked_by", verbose_name="News")
    is_like = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'news')
        verbose_name = "Like"
        verbose_name_plural = "Likes"

    def __str__(self):
        return f"{self.user.username} liked {self.news.title}"


# CommentLike Model
class CommentLike(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comment_likes', verbose_name='User')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes', verbose_name='Comment')
    is_like = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'comment')

    def __str__(self):
        return f"{self.user.username} {'liked' if self.is_like else 'disliked'} Comment {self.comment.id}"


class SavedArticle(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='saved_articles',
        verbose_name='User',
    )
    news = models.ForeignKey(
        News,
        on_delete=models.CASCADE,
        related_name='saved_by',
        verbose_name='News',
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Saved at')

    class Meta:
        unique_together = ('user', 'news')
        ordering = ['-created_at']
        verbose_name = 'Saved article'
        verbose_name_plural = 'Saved articles'

    def __str__(self):
        return f'{self.user.username} saved {self.news.title}'
