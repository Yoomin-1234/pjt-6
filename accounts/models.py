from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    GENDER_CHOICES = [
        ('M', '남성'),
        ('F', '여성'),
    ]

    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, verbose_name='성별')
    age = models.PositiveIntegerField(null=True, blank=True, verbose_name='나이')
    weekly_reading_time = models.PositiveIntegerField(null=True, blank=True, verbose_name='주간 평균 독서 시간(시간)')
    annual_reading_count = models.PositiveIntegerField(null=True, blank=True, verbose_name='연간 독서량(권)')
    profile_img = models.ImageField(upload_to='profiles/', blank=True, null=True, verbose_name='프로필 사진')

    followings = models.ManyToManyField(                        # F611: 팔로우 기능을 위한 User 간 M:N 관계
        'self',
        symmetrical=False,
        related_name='followers',
        blank=True,
    )

    categories = models.ManyToManyField(                       # F628: 사용자 선호 장르(Category)와의 M:N 관계
        'books.Category',
        related_name='users',
        blank=True,
        verbose_name='관심 장르',
    )