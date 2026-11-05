from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash, get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST, require_safe
from .forms import CustomUserCreationForm, CustomUserChangeForm
# Create your views here.
User = get_user_model()

@require_http_methods(['GET', 'POST'])
def login(request):                              # F607: 로그인
    if request.user.is_authenticated:
        return redirect('books:index')

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('books:index')
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


@login_required
@require_POST
def logout(request):                             # F608: 로그아웃 (POST 요청만 허용)
    auth_logout(request)
    return redirect('books:index')


@login_required
@require_POST
def follow(request, user_pk):                    # F611: 팔로우 / 언팔로우 (POST 요청만 허용)
    person = get_object_or_404(User, pk=user_pk)
    if person != request.user:
        if person.followers.filter(pk=request.user.pk).exists():
            person.followers.remove(request.user)
        else:
            person.followers.add(request.user)
    return redirect('accounts:profile', person.username)


@login_required
@require_POST
def delete(request):                            # F613: 회원탈퇴 (POST 요청만 허용)
    request.user.delete()
    auth_logout(request)
    return redirect('books:index')


@login_required
@require_http_methods(['GET', 'POST'])
def change_password(request):                   # F614: 비밀번호 변경 (변경 후 강제 로그아웃 방지)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('books:index')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'accounts/change_password.html', {'form': form})


# ==========================================
# 회원가입 (F609)
# ==========================================
@require_http_methods(['GET', 'POST'])
def signup(request):

    # 이미 로그인한 사용자는 메인 페이지로 이동
    if request.user.is_authenticated:
        return redirect('books:index')

    if request.method == 'POST':
        form = CustomUserCreationForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            user = form.save()

            # 회원가입 성공 후 자동 로그인
            auth_login(request, user)

            return redirect('books:index')

    else:
        form = CustomUserCreationForm()

    context = {
        'form': form,
    }

    return render(request, 'accounts/signup.html', context)


# ==========================================
# 프로필 (F610)
# ==========================================
@require_safe
def profile(request, username):

    # URL의 username으로 사용자를 조회
    person = get_object_or_404(User, username=username)

    # 해당 사용자가 작성한 쓰레드 조회
    threads = person.threads.select_related(
        'book'
    ).prefetch_related(
        'likes'
    ).all()

    # 현재 로그인한 사용자가 대상 사용자를 팔로우하는지 확인
    is_following = False

    if request.user.is_authenticated and request.user != person:
        is_following = person.followers.filter(
            pk=request.user.pk
        ).exists()

    context = {
        'person': person,
        'threads': threads,

        # 팔로워 수
        'followers_count': person.followers.count(),

        # 팔로잉 수
        'followings_count': person.followings.count(),

        # 팔로우 여부
        'is_following': is_following,
    }

    return render(
        request,
        'accounts/profile.html',
        context
    )



# ==========================================
# 회원정보 수정 (F612)
# ==========================================
@login_required
@require_http_methods(['GET', 'POST'])
def update(request):

    if request.method == 'POST':
        form = CustomUserChangeForm(
            request.POST,
            request.FILES,
            instance=request.user,
        )

        if form.is_valid():
            form.save()
            return redirect('books:index')

    else:
        form = CustomUserChangeForm(
            instance=request.user
        )

    context = {
        'form': form,
    }

    return render(
        request,
        'accounts/update.html',
        context
    )




# # -------------------------------------------------------------------
# # 아래는 팀원 B 담당 영역 (F609 signup, F610 profile, F612 update)
# # 팀원 B의 코드와 병합 시 팀원 B의 구현본으로 교체됩니다.
# # -------------------------------------------------------------------
# @require_http_methods(['GET', 'POST'])
# def signup(request):
#     return render(request, 'accounts/signup.html')


# @require_safe
# def profile(request, username):
#     person = get_object_or_404(User, username=username)
#     return render(request, 'accounts/profile.html', {'person': person})


# @login_required
# @require_http_methods(['GET', 'POST'])
# def update(request):
#     return render(request, 'accounts/update.html')