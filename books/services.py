import base64
import json
import re
import uuid

import requests
from openai import OpenAI

from django.conf import settings
from django.core.files.base import ContentFile


# ==========================================
# GMS OpenAI Client
# ==========================================
def get_gms_client():

    api_key = getattr(settings, 'GMS_API_KEY', '')
    base_url = getattr(settings, 'GMS_BASE_URL', '')

    if not api_key:
        raise ValueError('GMS_API_KEY가 설정되지 않았습니다.')

    return OpenAI(
        api_key=api_key,
        base_url=base_url,
        timeout=120.0,
        max_retries=1,
    )


# ==========================================
# 감정 키워드 5개 추출 (F626)
# GPT-5-nano 사용
# ==========================================
def extract_thread_keywords(thread):

    client = get_gms_client()

    book_title = thread.book.title
    author = thread.book.author
    content = thread.content[:6000]

    response = client.chat.completions.create(
        model='gpt-5-nano',
        messages=[
            {
                'role': 'system',
                'content': (
                    '너는 도서 감상문을 분석하는 전문가다. '
                    '도서와 독서 감상문에서 느껴지는 감정과 '
                    '분위기를 시각화하기 좋은 키워드 5개를 추출한다. '
                    '반드시 JSON 객체로만 응답한다. '
                    '형식은 {"keywords": ["키워드1", "키워드2", '
                    '"키워드3", "키워드4", "키워드5"]} 이다.'
                ),
            },
            {
                'role': 'user',
                'content': (
                    f'도서 제목: {book_title}\n'
                    f'저자: {author}\n'
                    f'독서 감상문: {content}\n\n'
                    '이미지 생성에 활용할 감정 및 시각적 키워드 '
                    '5개를 추출해 줘.'
                ),
            },
        ],
    )

    result = response.choices[0].message.content

    # JSON 부분 추출
    match = re.search(r'\{.*\}', result, re.DOTALL)

    if not match:
        raise ValueError('AI 키워드 응답을 JSON으로 해석할 수 없습니다.')

    data = json.loads(match.group())

    keywords = data.get('keywords', [])

    if not isinstance(keywords, list):
        raise ValueError('키워드 응답 형식이 올바르지 않습니다.')

    keywords = [
        str(keyword).strip()
        for keyword in keywords
        if str(keyword).strip()
    ]

    if len(keywords) < 5:
        raise ValueError('AI가 키워드 5개를 추출하지 못했습니다.')

    return keywords[:5]


# ==========================================
# 이미지 생성 프롬프트 작성 (F626)
# ==========================================
def create_cover_prompt(thread, keywords):

    book_title = thread.book.title
    author = thread.book.author

    keyword_text = ', '.join(keywords)

    prompt = f"""
    Create a beautiful and artistic book-inspired cover illustration.

    Book title: {book_title}
    Author: {author}

    Emotional and visual keywords:
    {keyword_text}

    Create an artistic illustration that expresses the emotions,
    atmosphere, and themes of the reading experience.

    Requirements:
    - Square composition.
    - High quality editorial book cover illustration.
    - Beautiful cinematic lighting.
    - Visually meaningful composition.
    - Rich details and artistic atmosphere.
    - Do not include text, letters, words, or watermarks.
    - Do not use copyrighted logos or recognizable characters.
    """

    return prompt


# ==========================================
# AI 커버 이미지 생성 및 저장 (F626)
# DALL-E 3 사용
# ==========================================


def generate_thread_cover(thread):

    client = get_gms_client()

    # 1. 감정 키워드 5개 추출
    keywords = extract_thread_keywords(thread)

    # 2. 이미지 생성 프롬프트 작성
    prompt = create_cover_prompt(thread, keywords)

    # 3. GMS 이미지 생성 API 호출
    # 기존 dall-e-3에서 실제 테스트에 성공한 모델로 변경
    response = client.images.generate(
        model="gpt-image-2.5-sunburst",
        prompt=prompt,
    )

    # 4. 이미지 데이터 확인
    if not response.data:
        raise ValueError("이미지 생성 결과가 없습니다.")

    image_data = response.data[0]

    # 5. 이미지 데이터 가져오기
    if image_data.b64_json:

        # Base64 이미지 데이터 디코딩
        image_bytes = base64.b64decode(image_data.b64_json)

    elif image_data.url:

        # 이미지 URL로 반환된 경우 다운로드
        image_response = requests.get(
            image_data.url,
            timeout=60,
        )

        image_response.raise_for_status()

        image_bytes = image_response.content

    else:
        raise ValueError("생성된 이미지 데이터가 없습니다.")

    # 6. 파일명 생성
    filename = f"thread_{thread.pk}_" f"{uuid.uuid4().hex[:8]}.png"

    # 7. Thread.cover_image 필드에 이미지 저장
    thread.cover_image.save(
        filename,
        ContentFile(image_bytes),
        save=True,
    )

    # 8. 추출한 키워드 반환
    return keywords
