
from django.db import models
from django.conf import settings


# ==========================================
# Category Model (F628)
# ==========================================
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


# ==========================================
# Book Model (F604, F625)
# ==========================================
class Book(models.Model):
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
    customer_review_rank = models.IntegerField(
        verbose_name='Customer review rank'
    )
    author = models.CharField(max_length=50, verbose_name='Author')

    # AI 작가 정보
    author_info = models.TextField(blank=True, default='')
    author_works = models.TextField(blank=True, default='')
    author_profile_img = models.URLField(blank=True, default='')

    def __str__(self):
        return self.title


# ==========================================
# Thread Model (F605)
# ==========================================
class Thread(models.Model):

    # 어떤 도서에 작성된 쓰레드인지
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='threads',
    )

    # 쓰레드 작성자
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='threads',
    )

    # 쓰레드 제목
    title = models.CharField(
        max_length=100,
        verbose_name='쓰레드 제목',
    )

    # 쓰레드 본문
    content = models.TextField(
        verbose_name='본문',
    )

    # 독서일
    reading_date = models.DateField(
        verbose_name='독서일',
    )

    # AI 생성 커버 이미지 (F626)
    cover_image = models.ImageField(
        upload_to='threads/',
        blank=True,
        null=True,
    )

    # 좋아요를 누른 사용자 (F624)
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='liked_threads',
        blank=True,
    )

    # 생성 시각
    created_at = models.DateTimeField(auto_now_add=True)

    # 수정 시각
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at', '-pk')

    def __str__(self):
        return self.title

    @property
    def like_count(self):
        return self.likes.count()


# ==========================================
# Comment Model (F627)
# ==========================================
class Comment(models.Model):

    # 댓글이 작성된 쓰레드
    thread = models.ForeignKey(
        Thread,
        on_delete=models.CASCADE,
        related_name='comments',
    )

    # 댓글 작성자
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
    )

    # 댓글 내용
    content = models.CharField(
        max_length=500,
        verbose_name='댓글 내용',
    )

    # 댓글 작성 시각
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at', 'pk')

    def __str__(self):
        return f'{self.user} - {self.content[:30]}'
