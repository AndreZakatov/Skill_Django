from django.core.management.base import BaseCommand
from blogapp.models import Article, Category, Tag, Author

class Command(BaseCommand):
    help = 'Создаёт тестовые статьи'

    def handle(self, *args, **options):
        author, _ = Author.objects.get_or_create(name='Тестовый автор')
        category, _ = Category.objects.get_or_create(name='Новости')
        tag1, _ = Tag.objects.get_or_create(name='Django')
        tag2, _ = Tag.objects.get_or_create(name='Python')

        article = Article.objects.create(
            title='Первая статья',
            content='Текст первой статьи',
            author=author,
            category=category,
        )
        article.tags.add(tag1, tag2)

        self.stdout.write(self.style.SUCCESS('Статья успешно создана!'))