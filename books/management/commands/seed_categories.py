
from django.core.management.base import BaseCommand
from books.models import Category


class Command(BaseCommand):
    help = '프로젝트 기본 도서 카테고리 등록'

    CATEGORIES = [
        '소설/시/희곡',
        '경제/경영',
        '자기계발',
        '인문/교양',
        '취미/실용',
        '어린이/청소년',
        '과학',
    ]

    def handle(self, *args, **options):

        for name in self.CATEGORIES:

            category, created = Category.objects.get_or_create(
                name=name
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'카테고리 생성 완료: {name}'
                    )
                )
            else:
                self.stdout.write(
                    f'이미 존재하는 카테고리: {name}'
                )

        self.stdout.write(
            self.style.SUCCESS('카테고리 등록 작업 완료!')
        )
