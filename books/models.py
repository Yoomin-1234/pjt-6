from django.db import models
from django.conf import settings

# Create your models here.

class Category(models.Model):              # F628: 도서 및 사용자 선호 장르 카테고리 모델 (팀원 B 연동용)
    name = models.CharField(max_length=50, unique=True)

class Book(models.Model):                  # F604 & F625: Book 모델
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='books',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='books',
        verbose_name='Category',
    )
    title = models.CharField(max_length=100, verbose_name='Title')
    description = models.TextField(verbose_name='Description')
    customer_review_rank = models.IntegerField(verbose_name='Customer review rank')
    author = models.CharField(max_length=50, verbose_name='Author')
    author_info = models.TextField(blank=True, default='')           # F625: 생성형 AI 작가 정보 및 대표작 저장 필드
    author_works = models.TextField(blank=True, default='')
    author_profile_img = models.URLField(blank=True, default='')

# class Thread(models.Model):         # F605, F624, F626: Thread 모델 (Book 상세 페이지 연동용 기본 스키마)
#     book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='threads')
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='threads')
#     title = models.CharField(max_length=100)
#     content = models.TextField()
#     reading_date = models.DateField()
#     cover_image = models.ImageField(upload_to='threads/', blank=True, null=True)
#     likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_threads', blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

# class Comment(models.Model):         # F627: 쓰레드 댓글 모델
#     thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='comments')
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
#     content = models.CharField(max_length=200)
#     created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):          # F627: 쓰레드 댓글 모델
    thread = models.ForeignKey(
        'books.Thread',
        on_delete=models.CASCADE,
        related_name='comments',
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    content = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)