# 📚 06-PJT: 관계형 DB 설계 기반 AI 도서 분석 및 커뮤니티 서비스 (ThRead)

## 📌 프로젝트 개요

본 프로젝트는 **Django 관계형 데이터베이스(`1:N`, `M:N`) 설계**와 **Django Authentication System**, 그리고 **생성형 AI API(`gpt-5-nano`, `dall-e-3`) 및 Wikipedia API**를 결합하여 구축한 도서 분석 및 독서 감상(Thread) 공유 웹 애플리케이션입니다.

사용자는 도서 데이터를 등록·조회·수정·삭제할 수 있으며, 도서 등록 시 AI가 작가 정보와 대표작을 자동으로 생성합니다. 또한 도서별 독서 감상 쓰레드(Thread)를 작성할 때 AI가 감정을 분석하여 맞춤형 커버 이미지를 생성해 주며, 사용자 간 팔로우, 쓰레드 좋아요, 댓글, 선호 장르(카테고리) 기반 필터링 등 풍부한 커뮤니티 기능을 제공합니다.

---

## 🛠️ 기술 스택 및 개발 환경 (Tech Stack)

* **Language**: Python 3.11
* **Framework**: Django 5.2.5
* **Frontend / Styling**: HTML5, CSS3, Bootstrap 5.3.3
* **Database**: SQLite3
* **External API & AI**:
  * Wikipedia REST API (작가 요약 정보 및 프로필 이미지 조회)
  * SSAFY GMS / OpenAI API (`gpt-5-nano`: 작가 정보 생성 및 쓰레드 감정 키워드 추출, `dall-e-3`: 쓰레드 커버 이미지 생성)
* **Libraries**: `openai`, `requests`, `Pillow`, `python-dotenv`

---

## 👥 역할 분담표 (Role Distribution)

2인 협업을 진행하며 코드 충돌을 최소화하고, 관계형 데이터베이스 모델 설계부터 View, Form, Template, AI 연동까지 전 과정을 균형 있게 경험할 수 있도록 아래와 같이 역할을 분담했습니다.

| 요구사항 | 기능명 | 담당 | 구현 상세 요약 |
| :---: | :--- | :---: | :--- |
| **F601** | 프로젝트 구성 | **소준호** | `mypjt` 프로젝트 및 `accounts`, `books` 앱 생성, 공통 `base.html` 및 Navbar 구성 |
| **F602** | `accounts` Model Class | **소준호** | `AbstractUser` 상속 커스텀 `User` 모델, 프로필 이미지 및 팔로우(`M:N`), 선호 카테고리(`M:N`) 설계 |
| **F603** | `accounts` Form Class | **김유민** | `CustomUserCreationForm`, `CustomUserChangeForm` 구현 및 선호 카테고리 다중 선택 위젯 적용 |
| **F604** | `Book` Model Class | **소준호** | 도서 기본 정보, 작성자(`User`와 `1:N`), 카테고리(`Category`와 `1:N`), AI 작가 정보 필드 설계 |
| **F605** | `Thread` Model Class | **김유민** | 도서(`Book`과 `N:1`), 작성자(`User`와 `N:1`), 좋아요(`User`와 `M:N`), AI 커버 이미지 필드 설계 |
| **F606** | `books` Form Class | **김유민** | 데이터 검증 및 에러 메시지 관리를 위한 `BookForm`, `ThreadForm`, `CommentForm` 구현 |
| **F607** | 로그인 (`login`) | **소준호** | `AuthenticationForm` 기반 로그인 검증, 세션 생성 및 로그인 전후 동적 Navbar 전환 |
| **F608** | 로그아웃 (`logout`) | **소준호** | `POST` 요청 전용 현재 인증된 사용자의 세션 삭제 처리 |
| **F609** | 회원가입 (`signup`) | **김유민** | 신규 회원 데이터 및 프로필 사진, 선호 장르 검증·저장 후 자동 로그인 처리 |
| **F610** | 프로필 (`profile`) | **김유민** | 회원 기본 정보, 선호 장르, 작성한 쓰레드 목록, 팔로워/팔로잉 수 및 조건부 버튼 출력 |
| **F611** | 팔로우 (`follow`) | **소준호** | 타 사용자 프로필에서 `POST` 요청을 통한 팔로우 / 언팔로우 토글 기능 |
| **F612** | 회원정보 수정 (`update`) | **김유민** | 로그인 사용자의 개인정보, 프로필 이미지, 선호 장르 수정 및 기존 선택값(`initial`) 유지 |
| **F613** | 회원탈퇴 (`delete`) | **소준호** | `POST` 요청 기반 인증된 사용자의 계정 삭제 및 로그아웃 처리 |
| **F614** | 비밀번호 변경 (`change_password`) | **소준호** | `PasswordChangeForm` 활용 비밀번호 변경 및 `update_session_auth_hash`로 세션 유지 |
| **F615** | 도서 목록 (`index`) | **김유민** | 전체 도서 목록 조회 및 카테고리별 도서 필터링 기능 제공 |
| **F616** | 도서 등록 (`create`) | **소준호** | 로그인 사용자 전용 도서 생성, 작성자(`1:N`) 연결 및 AI 작가 정보 자동 생성 연동 |
| **F617** | 도서 상세 (`detail`) | **소준호** | 단일 도서 정보, AI 생성 작가 정보, 종속된 쓰레드 목록 조회 및 작성자 전용 수정/삭제 버튼 표시 |
| **F618** | 도서 수정 (`update`) | **소준호** | 도서 작성자 본인 검증 후 기존 도서 데이터 수정 처리 |
| **F619** | 도서 삭제 (`delete`) | **소준호** | 도서 작성자 본인 검증 및 `POST` 요청 시 단일 도서 데이터 삭제 |
| **F620** | 쓰레드 등록 (`thread_create`) | **김유민** | 대상 도서(`Book`) 및 작성자(`User`)와 `N:1` 관계를 맺는 독서 감상 쓰레드 생성 |
| **F621** | 쓰레드 상세 (`thread_detail`) | **김유민** | 쓰레드 본문, 독서일, AI 커버 이미지, 좋아요 수, 댓글 목록 조회 및 작성자 전용 버튼 출력 |
| **F622** | 쓰레드 수정 (`thread_update`) | **김유민** | 쓰레드 작성자 본인 검증 후 독서 감상 데이터 수정 |
| **F623** | 쓰레드 삭제 (`thread_delete`) | **김유민** | 쓰레드 작성자 본인 검증 및 `POST` 요청 시 쓰레드 삭제 후 도서 상세 페이지로 리다이렉트 |
| **F624** | 쓰레드 좋아요 (`like`) | **김유민** | `POST` 요청 기반 쓰레드 좋아요 추가 및 취소(`M:N`) 토글 처리 |
| **F625** | AI 작가 정보 생성 (심화) | **소준호** | Wikipedia API 조회 결과와 도서 정보를 조합해 `gpt-5-nano`로 작가 소개 및 대표작(JSON) 생성·저장 |
| **F626** | AI 커버 이미지 생성 (심화) | **김유민** | `gpt-5-nano`로 쓰레드 감정 키워드 5개를 추출하고 `dall-e-3`로 커버 이미지를 생성해 파일 저장 |
| **F627** | 쓰레드 댓글 (심화) | **김유민** | 쓰레드 상세 페이지 내 댓글 생성, 작성자 프로필 이동 링크, 본인 댓글 삭제(`POST`) 구현 |
| **F628** | 카테고리 (심화) | **김유민** | 7대 장르 `Category` 모델 구현, 초기 시드 커맨드(`seed_categories`) 작성, 회원(`M:N`) 및 도서(`1:N`) 연결 |
| **NF601** | Git 활용 및 프로젝트 관리 | **소준호** | 브랜치 전략 수립, 커밋 컨벤션 정의, 병합(Merge) 관리 및 히스토리 정리 |
| **NF602** | URL 구성 및 유지보수 | **소준호** | `app_name` 네임스페이스와 `name`을 활용한 URL 역참조 구성 |
| **NF603** | HTTP Method 제한 기준 관리 | **소준호** | `@require_safe`, `@require_POST`, `@require_http_methods`, `@login_required` 일괄 적용 |

---

## 📂 디렉토리 구조 (Directory Structure)

```text
06-pjt/
├── accounts/
│   ├── migrations/
│   ├── forms.py                          # CustomUserCreationForm, CustomUserChangeForm
│   ├── models.py                         # AbstractUser 상속 User 모델 (팔로우 M:N, 카테고리 M:N)
│   ├── urls.py                           # accounts 앱 URL 라우팅
│   ├── views.py                          # 인증(로그인/아웃/가입/수정/탈퇴/비밀번호) 및 프로필/팔로우
│   └── templates/accounts/
│       ├── login.html                    # 로그인 페이지
│       ├── change_password.html          # 비밀번호 변경 페이지
│       ├── signup.html                   # 회원가입 페이지 (프로필 사진, 관심 장르 포함)
│       ├── update.html                   # 회원정보 수정 페이지
│       └── profile.html                  # 개인 프로필 페이지 (팔로우/언팔로우, 작성 쓰레드 출력)
├── books/
│   ├── management/commands/
│   │   └── seed_categories.py            # 7대 장르 카테고리 초기 데이터 시딩 커맨드
│   ├── migrations/
│   ├── forms.py                          # BookForm, ThreadForm, CommentForm
│   ├── models.py                         # Category, Book, Thread, Comment 모델 정의
│   ├── services.py                       # Wikipedia API, gpt-5-nano 작가 정보, dall-e-3 커버 생성
│   ├── urls.py                           # books 앱 URL 라우팅
│   ├── views.py                          # 도서 CRUD, 쓰레드 CRUD, 좋아요, 댓글, 카테고리 필터
│   └── templates/books/
│       ├── index.html                    # 메인 도서 목록 및 카테고리 필터 탭
│       ├── create.html                   # 도서 등록 페이지
│       ├── detail.html                   # 도서 상세 페이지 (AI 작가 정보, 쓰레드 목록 포함)
│       ├── update.html                   # 도서 수정 페이지
│       ├── thread_create.html            # 쓰레드 작성 페이지
│       ├── thread_detail.html            # 쓰레드 상세 페이지 (AI 커버 이미지, 좋아요, 댓글 포함)
│       └── thread_update.html            # 쓰레드 수정 페이지
├── media/
│   ├── profiles/                         # 업로드된 사용자 프로필 이미지 저장 경로
│   └── threads/                          # dall-e-3로 생성된 쓰레드 커버 이미지 저장 경로
├── mypjt/                                # 프로젝트 전역 설정 (settings.py, urls.py)
├── results/                              # 요구사항별 실행 결과 및 Git 커밋 스크린샷 폴더
├── templates/
│   └── base.html                         # 공통 네비게이션바 및 기본 레이아웃
├── .env.example                          # 환경변수 예시 파일 (GMS_API_KEY)
├── .gitignore
├── manage.py
├── requirements.txt
└── README.md
```

---

## 🚀 프로젝트 실행 방법 (How to Run)

```bash
# 1. 가상환경 생성 및 활성화 (Python 3.11)
python -m venv venv
source venv/Scripts/activate  # Windows 기준 (Mac/Linux: source venv/bin/activate)

# 2. 필수 패키지 설치
pip install -r requirements.txt

# 3. 환경변수(.env) 설정
# 루트 폴더에 .env 파일을 생성하고 GMS_API_KEY 입력
cp .env.example .env

# 4. 데이터베이스 마이그레이션 및 7대 장르 카테고리 초기 데이터 시딩 (F628)
python manage.py makemigrations
python manage.py migrate
python manage.py seed_categories

# 5. 개발 서버 실행
python manage.py runserver
```
---

## 💬 팀원별 회고 및 느낀 점 (Reflections)

### 👤 소준호
* **담당 역할**: 프로젝트 초기 세팅(`F601`), `User`·`Book` 모델 설계(`F602`, `F604`), 회원 인증 및 팔로우(`F607`, `F608`, `F611`, `F613`, `F614`), 도서 CRUD(`F616`~`F619`), AI 작가 정보 생성(`F625`), Git 및 보안 관리(`NF601`~`NF603`)
* **느낀 점**:
  * 프로젝트 초기 환경 구축과 관계형 모델 설계, 회원 인증 및 팔로우 기능, 그리고 도서 CRUD와 AI 작가 정보 생성 파이프라인 구현을 담당했습니다. 이전 회차에서 다뤘던 기본 인증과 도서 관리 기능에 더해, 작성자(1:N) 권한 검증과 팔로우(M:N) 기능을 직접 연결해 보면서 실제 커뮤니티 서비스의 데이터베이스가 어떻게 동작하는지 이해하는데 도움이 되었습니다. 또한 도서를 등록할 때 GMS를 활용해 작가 소개와 대표작을 자동으로 채워주는 기능을 구현하면서, 외부 API 오류나 동명이인 예외 상황에서도 도서 등록이 중단되지 않도록 설계하는 경험이 재미있었습니다.

### 👤 김유민
* **담당 역할**: 회원/도서/쓰레드 Form 구현(`F603`, `F606`), `Thread`·`Comment`·`Category` 모델 설계(`F605`, `F627`, `F628`), 회원가입·프로필·정보수정(`F609`, `F610`, `F612`), 도서 목록 및 카테고리 필터링(`F615`), 쓰레드 CRUD·좋아요·댓글(`F620`~`F624`, `F627`), AI 커버 이미지 생성(`F626`)
* **느낀 점**:
  * 계층적 구조를 구현하면서 URL 파라미터전달과 외래키 데이터 무결성 처리에 대해 배울 수 있었습니다. Category 모델을 별도로 분리하여 사용자와는 M:N, 도서와는 1:N으로 연결하고 seed_categories 커맨드로 초기 데이터를 자동화해 본 과정이 유익했습니다. 쓰레드 작성 시 GMS로 독서 감상의 감정 키워드를 추출하고 커버 이미지를 생성·저장하는 2단계 AI 파이프라인을 완성하면 재미와 성취감을 느꼈고, 팀원과 사전에 모델과 인터페이스를 맞춘 덕분에 수월하게 프로젝트를 마무리할 수 있었습니다.
