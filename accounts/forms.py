from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


# 공통 Bootstrap 스타일 적용


def add_bootstrap_style(form):
    for field in form.fields.values():

        # 체크박스 그룹에는 form-check-input을 적용하지 않음
        # 개별 체크박스 스타일은 HTML 템플릿에서 처리
        if isinstance(field.widget, forms.CheckboxSelectMultiple):
            field.widget.attrs.pop("class", None)

        elif isinstance(field.widget, forms.Select):
            field.widget.attrs.update(
                {
                    "class": "form-select",
                }
            )

        else:
            field.widget.attrs.update(
                {
                    "class": "form-control",
                }
            )


# ==========================================
# 회원가입 Form (F603, F609)
# ==========================================
class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User

        fields = (
            'username',
            'email',
            'last_name',
            'first_name',
            'gender',
            'age',
            'weekly_reading_time',
            'annual_reading_count',
            'profile_img',
            'categories',
        )

        labels = {
            'username': '아이디',
            'email': '이메일',
            'last_name': '성',
            'first_name': '이름',
            'gender': '성별',
            'age': '나이',
            'weekly_reading_time': '주간 평균 독서 시간',
            'annual_reading_count': '연간 독서량',
            'profile_img': '프로필 사진',
            'categories': '선호 장르',
        }

        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': '아이디를 입력하세요.',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': '이메일을 입력하세요.',
            }),
            'age': forms.NumberInput(attrs={
                'min': 0,
            }),
            'weekly_reading_time': forms.NumberInput(attrs={
                'min': 0,
            }),
            'annual_reading_count': forms.NumberInput(attrs={
                'min': 0,
            }),
            'categories': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 이메일 필수 입력
        self.fields['email'].required = True

        # 비밀번호 안내 문구
        self.fields['password1'].label = '비밀번호'
        self.fields['password2'].label = '비밀번호 확인'

        # 필드 순서 지정
        self.order_fields([
            'username',
            'password1',
            'password2',
            'email',
            'last_name',
            'first_name',
            'gender',
            'age',
            'weekly_reading_time',
            'annual_reading_count',
            'profile_img',
            'categories',
        ])

        add_bootstrap_style(self)


# ==========================================
# 회원정보 수정 Form (F603, F612)
# ==========================================
class CustomUserChangeForm(forms.ModelForm):

    class Meta:
        model = User

        fields = (
            'email',
            'last_name',
            'first_name',
            'gender',
            'age',
            'weekly_reading_time',
            'annual_reading_count',
            'profile_img',
            'categories',
        )

        labels = {
            'email': '이메일',
            'last_name': '성',
            'first_name': '이름',
            'gender': '성별',
            'age': '나이',
            'weekly_reading_time': '주간 평균 독서 시간',
            'annual_reading_count': '연간 독서량',
            'profile_img': '프로필 사진',
            'categories': '선호 장르',
        }

        widgets = {
            'email': forms.EmailInput(),
            'age': forms.NumberInput(attrs={
                'min': 0,
            }),
            'weekly_reading_time': forms.NumberInput(attrs={
                'min': 0,
            }),
            'annual_reading_count': forms.NumberInput(attrs={
                'min': 0,
            }),
            'categories': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].required = True

        add_bootstrap_style(self)
