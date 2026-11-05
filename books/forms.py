from django import forms
from .models import Book, Thread, Comment


# ==========================================
# Book Form (F606)
# ==========================================
class BookForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = (
            'category',
            'title',
            'description',
            'customer_review_rank',
            'author',
        )

        labels = {
            'category': '카테고리',
            'title': '도서 제목',
            'description': '도서 설명',
            'customer_review_rank': '회원 리뷰 평점',
            'author': '저자',
        }

        widgets = {
            'description': forms.Textarea(attrs={
                'rows': 5,
            }),
        }


# ==========================================
# Thread Form (F606)
# ==========================================
class ThreadForm(forms.ModelForm):

    class Meta:
        model = Thread
        fields = (
            'title',
            'content',
            'reading_date',
        )

        labels = {
            'title': '쓰레드 제목',
            'content': '본문',
            'reading_date': '독서일',
        }

        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 5,
            }),
            'reading_date': forms.DateInput(attrs={
                'type': 'date',
            }),
        }


# ==========================================
# Comment Form (F627)
# ==========================================
class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('content',)

        labels = {
            'content': '댓글',
        }

        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': '댓글을 입력하세요.',
            }),
        }
