from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST, require_safe
from .models import Book, Thread, Category, Comment
from .forms import BookForm, ThreadForm, CommentForm


# Create your views here.


# ==========================================
# 도서 등록 (F616, F625 연동)
# ==========================================
@login_required
@require_http_methods(["GET", "POST"])
def create(request):

    if request.method == "POST":

        form = BookForm(request.POST, request.FILES)

        if form.is_valid():

            book = form.save(commit=False)
            book.user = request.user
            book.save()

            # AI 작가 정보 생성
            # 현재 A 담당 서비스가 완성되지 않아도
            # 도서 등록은 정상적으로 진행되도록 처리
            try:
                from .services import fetch_author_ai_info

                ai_data = fetch_author_ai_info(
                    book.author, book.title, book.description
                )

                book.author_info = ai_data.get("author_info", "")

                book.author_works = ai_data.get("author_works", "")

                book.author_profile_img = ai_data.get("author_profile_img", "")

                book.save()

            except Exception:
                import logging

                logging.exception("AI 작가 정보 생성 실패")

            return redirect("books:detail", pk=book.pk)

    else:
        form = BookForm()

    return render(request, "books/create.html", {"form": form})


# ==========================================
# 도서 상세 조회 (F617)
# ==========================================
@require_safe
def detail(request, pk):

    # 도서 조회
    book = get_object_or_404(Book, pk=pk)

    # 해당 도서에 작성된 쓰레드 조회
    threads = book.threads.all()

    context = {
        "book": book,
        "threads": threads,
    }

    return render(request, "books/detail.html", context)


@login_required
@require_http_methods(['GET', 'POST'])
def update(request, pk):                   # F618: 도서 수정 (작성자 본인만 가능)
    book = get_object_or_404(Book, pk=pk)
    if request.user != book.user:
        return redirect('books:detail', book.pk)

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('books:detail', book.pk)
    else:
        form = BookForm(instance=book)

    context = {
        'book': book,
        'form': form,
    }
    return render(request, 'books/update.html', context)


@login_required
@require_POST
def delete(request, pk):                  # F619: 도서 삭제 (작성자 본인만 가능, POST 요청만 허용)
    book = get_object_or_404(Book, pk=pk)
    if request.user == book.user:
        book.delete()
        return redirect('books:index')
    return redirect('books:detail', book.pk)


# ==========================================
# 도서 목록 (F615)
# ==========================================
@require_safe
def index(request):

    # 전체 도서 조회
    books = Book.objects.select_related(
        'user',
        'category'
    ).order_by('-pk')

    # 전체 카테고리 조회
    categories = Category.objects.all()

    # 선택한 카테고리 확인
    selected_category = request.GET.get('category', '').strip()

    selected_category_id = None

    # 카테고리별 도서 필터링
    if selected_category.isdigit():
        selected_category_id = int(selected_category)
        books = books.filter(
            category_id=selected_category_id
        )

    context = {
        'books': books,
        'categories': categories,
        'selected_category_id': selected_category_id,
    }

    return render(
        request,
        'books/index.html',
        context
    )


# ==========================================
# 쓰레드 등록 (F620)
# ==========================================
@login_required
@require_http_methods(['GET', 'POST'])
def thread_create(request, book_pk):

    # URL에서 전달받은 도서 조회
    book = get_object_or_404(Book, pk=book_pk)

    # POST 요청: 쓰레드 작성
    if request.method == 'POST':

        form = ThreadForm(request.POST)

        if form.is_valid():

            # 아직 DB에 저장하지 않고 객체 생성
            thread = form.save(commit=False)

            # 현재 로그인한 사용자 연결
            thread.user = request.user

            # 해당 도서 연결
            thread.book = book

            # DB 저장
            thread.save()

            # AI 커버 이미지 생성
            try:
                from .services import generate_thread_cover

                generate_thread_cover(thread)

            except Exception:
                import logging

                logging.exception(
                    'AI 커버 이미지 생성 실패: thread_id=%s',
                    thread.pk
                )

            # 커버 생성 실패와 관계없이 쓰레드 등록 완료
            return redirect(
                'books:thread_detail',
                book_pk=book.pk,
                thread_pk=thread.pk,
            )

    # GET 요청: 빈 작성 Form 출력
    else:
        form = ThreadForm()

    context = {
        'book': book,
        'form': form,
    }

    return render(
        request,
        'books/thread_create.html',
        context
    )


# ==========================================
# 쓰레드 상세 조회 (F621)
# ==========================================
@require_safe
def thread_detail(request, book_pk, thread_pk):

    # 해당 도서 조회
    book = get_object_or_404(Book, pk=book_pk)

    # 해당 도서에 속한 쓰레드 조회
    thread = get_object_or_404(
        Thread,
        pk=thread_pk,
        book=book
    )

    # 좋아요 여부 확인
    is_liked = False

    if request.user.is_authenticated:
        is_liked = thread.likes.filter(
            pk=request.user.pk
        ).exists()

    # 해당 쓰레드의 댓글 조회
    comments = thread.comments.select_related(
        'user'
    ).all()

    # 댓글 작성 Form
    comment_form = CommentForm()

    context = {
        'book': book,
        'thread': thread,
        'is_liked': is_liked,
        'comments': comments,
        'comment_form': comment_form,
    }

    return render(
        request,
        'books/thread_detail.html',
        context
    )


# ==========================================
# 쓰레드 수정 (F622)
# ==========================================
@login_required
@require_http_methods(['GET', 'POST'])
def thread_update(request, book_pk, thread_pk):

    # 해당 도서 조회
    book = get_object_or_404(
        Book,
        pk=book_pk
    )

    # 현재 로그인한 사용자가 작성한 쓰레드만 조회
    thread = get_object_or_404(
        Thread,
        pk=thread_pk,
        book=book,
        user=request.user
    )

    # POST 요청: 수정 데이터 처리
    if request.method == 'POST':

        form = ThreadForm(
            request.POST,
            instance=thread
        )

        if form.is_valid():
            form.save()

            return redirect(
                'books:thread_detail',
                book_pk=book.pk,
                thread_pk=thread.pk
            )

    # GET 요청: 기존 데이터 출력
    else:
        form = ThreadForm(
            instance=thread
        )

    context = {
        'book': book,
        'thread': thread,
        'form': form,
    }

    return render(
        request,
        'books/thread_update.html',
        context
    )


# ==========================================
# 쓰레드 삭제 (F623)
# ==========================================
@login_required
@require_http_methods(['POST'])
def thread_delete(request, book_pk, thread_pk):

    # 해당 도서 조회
    book = get_object_or_404(
        Book,
        pk=book_pk
    )

    # 현재 로그인한 사용자가 작성한 쓰레드만 조회
    thread = get_object_or_404(
        Thread,
        pk=thread_pk,
        book=book,
        user=request.user
    )

    # 쓰레드 삭제
    thread.delete()

    # 해당 도서의 상세 페이지로 이동
    return redirect(
        'books:detail',
        pk=book.pk
    )


# ==========================================
# 쓰레드 좋아요 (F624)
# ==========================================
@login_required
@require_POST
def like(request, book_pk, thread_pk):

    # 해당 도서 조회
    book = get_object_or_404(
        Book,
        pk=book_pk
    )

    # 해당 도서에 속한 쓰레드 조회
    thread = get_object_or_404(
        Thread,
        pk=thread_pk,
        book=book
    )

    # 이미 좋아요를 눌렀는지 확인
    if thread.likes.filter(
        pk=request.user.pk
    ).exists():

        # 이미 좋아요를 눌렀다면 취소
        thread.likes.remove(request.user)

    else:

        # 좋아요를 누르지 않았다면 추가
        thread.likes.add(request.user)

    # 현재 쓰레드 상세 페이지로 이동
    return redirect(
        'books:thread_detail',
        book_pk=book.pk,
        thread_pk=thread.pk
    )


# ==========================================
# 댓글 작성 (F627)
# ==========================================
@login_required
@require_POST
def comment_create(request, book_pk, thread_pk):

    # 도서 조회
    book = get_object_or_404(
        Book,
        pk=book_pk
    )

    # 쓰레드 조회
    thread = get_object_or_404(
        Thread,
        pk=thread_pk,
        book=book
    )

    # 댓글 Form
    form = CommentForm(request.POST)

    if form.is_valid():

        # DB 저장 전 객체 생성
        comment = form.save(commit=False)

        # 댓글 작성자 지정
        comment.user = request.user

        # 댓글이 작성된 쓰레드 지정
        comment.thread = thread

        # DB 저장
        comment.save()

        # 쓰레드 상세 페이지로 이동
        return redirect(
            'books:thread_detail',
            book_pk=book.pk,
            thread_pk=thread.pk
        )

    # 유효하지 않은 댓글인 경우 상세 페이지에 오류 표시
    comments = thread.comments.select_related(
        'user'
    ).all()

    is_liked = thread.likes.filter(
        pk=request.user.pk
    ).exists()

    context = {
        'book': book,
        'thread': thread,
        'comments': comments,
        'comment_form': form,
        'is_liked': is_liked,
    }

    return render(
        request,
        'books/thread_detail.html',
        context,
        status=400
    )


# ==========================================
# 댓글 삭제 (F627)
# ==========================================
@login_required
@require_POST
def comment_delete(request, book_pk, thread_pk, comment_pk):

    # 도서 조회
    book = get_object_or_404(
        Book,
        pk=book_pk
    )

    # 쓰레드 조회
    thread = get_object_or_404(
        Thread,
        pk=thread_pk,
        book=book
    )

    # 현재 로그인한 사용자가 작성한 댓글만 조회
    comment = get_object_or_404(
        Comment,
        pk=comment_pk,
        thread=thread,
        user=request.user
    )

    # 댓글 삭제
    comment.delete()

    # 쓰레드 상세 페이지로 이동
    return redirect(
        'books:thread_detail',
        book_pk=book.pk,
        thread_pk=thread.pk
    )


# @require_safe
# def thread_detail(request, book_pk, thread_pk):
#     return redirect('books:detail', book_pk)


# @login_required
# @require_http_methods(['GET', 'POST'])
# def thread_update(request, book_pk, thread_pk):
#     return redirect('books:detail', book_pk)


# @login_required
# @require_POST
# def thread_delete(request, book_pk, thread_pk):
#     return redirect('books:detail', book_pk)


# @login_required
# @require_POST
# def like(request, book_pk, thread_pk):
#     return redirect('books:thread_detail', book_pk, thread_pk)
