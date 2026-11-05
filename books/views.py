from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST, require_safe
from .models import Book, Thread, Category
from .forms import BookForm
from .services import fetch_author_ai_info

# Create your views here.
@login_required
@require_http_methods(['GET', 'POST'])
def create(request):                        # F616 & F625: 도서 등록 및 AI 작가 정보 생성
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.user = request.user
            ai_data = fetch_author_ai_info(book.author, book.title, book.description)
            book.author_info = ai_data['author_info']
            book.author_works = ai_data['author_works']
            book.author_profile_img = ai_data['author_profile_img']
            book.save()
            return redirect('books:detail', book.pk)
    else:
        form = BookForm()

    return render(request, 'books/create.html', {'form': form})



@require_safe
def detail(request, pk):                   # F617 & F625: 단일 도서 상세 조회
    book = get_object_or_404(Book, pk=pk)
    threads = book.threads.all()
    context = {
        'book': book,
        'threads': threads,
    }
    return render(request, 'books/detail.html', context)



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


# # -------------------------------------------------------------------
# # 아래는 팀원 B 담당 영역 (index, thread_create, thread_detail, thread_update, thread_delete, like)
# # 팀원 B의 코드와 병합 전 서버 실행 확인용 기본 함수입니다.
# # -------------------------------------------------------------------
# @require_safe
# def index(request):
#     books = Book.objects.all()
#     return render(request, 'books/index.html', {'books': books})


# @login_required
# @require_http_methods(['GET', 'POST'])
# def thread_create(request, book_pk):
#     return redirect('books:detail', book_pk)


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