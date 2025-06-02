import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from reviews.models import Category, Comment, Genre, Review, Title, User


class Command(BaseCommand):
    help = 'Импорт данных из CSV файлов в базу YaMDb'

    def handle(self, *args, **options):
        data_dir = os.path.join(settings.BASE_DIR, 'static', 'data')

        self.stdout.write('Начинаю импорт данных...')
        any_success = False

        any_success |= self.import_users(os.path.join(data_dir, 'users.csv'))
        any_success |= self.import_categories(
            os.path.join(data_dir, 'category.csv'))
        any_success |= self.import_genres(os.path.join(data_dir, 'genre.csv'))
        any_success |= self.import_titles(os.path.join(data_dir, 'titles.csv'))
        any_success |= self.import_reviews(
            os.path.join(data_dir, 'review.csv'))
        any_success |= self.import_comments(
            os.path.join(data_dir, 'comments.csv'))

        if any_success:
            self.stdout.write(
                self.style.SUCCESS('Импорт данных завершён успешно.'))
        else:
            self.stdout.write(self.style.WARNING(
                'Импорт данных не выполнен: файлы не найдены.'))

    def import_users(self, path):
        if not os.path.exists(path):
            self.stdout.write(self.style.ERROR(f'Файл {path} не найден.'))
            return False

        count = 0
        with open(path, encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for user_data in reader:
                User.objects.update_or_create(
                    id=user_data['id'],
                    defaults={
                        'username': user_data['username'],
                        'email': user_data['email'],
                        'role': user_data.get('role', 'user') or 'user',
                        'bio': user_data.get('bio', ''),
                        'first_name': user_data.get('first_name', ''),
                        'last_name': user_data.get('last_name', ''),
                    }
                )
                count += 1
        self.stdout.write(f'Импортировано {count} пользователей из {path}')
        return True

    def import_categories(self, path):
        if not os.path.exists(path):
            self.stdout.write(self.style.ERROR(f'Файл {path} не найден.'))
            return False

        count = 0
        with open(path, encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for category_data in reader:
                Category.objects.update_or_create(
                    id=category_data['id'],
                    defaults={
                        'name': category_data['name'],
                        'slug': category_data['slug'],
                    }
                )
                count += 1
        self.stdout.write(f'Импортировано {count} категорий из {path}')
        return True

    def import_genres(self, path):
        if not os.path.exists(path):
            self.stdout.write(self.style.ERROR(f'Файл {path} не найден.'))
            return False

        count = 0
        with open(path, encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for genre_data in reader:
                Genre.objects.update_or_create(
                    id=genre_data['id'],
                    defaults={
                        'name': genre_data['name'],
                        'slug': genre_data['slug'],
                    }
                )
                count += 1
        self.stdout.write(f'Импортировано {count} жанров из {path}')
        return True

    def import_titles(self, path):
        if not os.path.exists(path):
            self.stdout.write(self.style.ERROR(f'Файл {path} не найден.'))
            return False

        count = 0
        with open(path, encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for title_data in reader:
                category = Category.objects.filter(
                    id=title_data['category']).first()
                if not category:
                    self.stdout.write(self.style.WARNING(
                        f'Категория с id {title_data["category"]}'
                        'не найдена для произведения {title_data["name"]}'
                    ))
                    continue

                Title.objects.update_or_create(
                    id=title_data['id'],
                    defaults={
                        'name': title_data['name'],
                        'year': title_data['year'],
                        'category': category,
                        'description': title_data.get('description', ''),
                    }
                )
                count += 1
        self.stdout.write(f'Импортировано {count} произведений из {path}')
        self.import_title_genres()
        return True

    def import_title_genres(self):
        path = os.path.join(settings.BASE_DIR, 'static',
                            'data', 'genre_title.csv')
        if not os.path.exists(path):
            self.stdout.write(self.style.ERROR(f'Файл {path} не найден.'))
            return False

        with open(path, encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for genre_title_data in reader:
                title = Title.objects.filter(
                    id=genre_title_data['title_id']).first()
                genre = Genre.objects.filter(
                    id=genre_title_data['genre_id']).first()
                if title and genre:
                    title.genre.add(genre)
                else:
                    self.stdout.write(self.style.WARNING(
                        "Не найдена связь жанр-произведение:"
                        f" title_id={genre_title_data['title_id']}"
                        f" genre_id={genre_title_data['genre_id']}"
                    ))
        return True

    def import_reviews(self, path):
        if not os.path.exists(path):
            self.stdout.write(self.style.ERROR(f'Файл {path} не найден.'))
            return False

        count = 0
        with open(path, encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for review_data in reader:
                title = Title.objects.filter(
                    id=review_data['title_id']).first()
                author = User.objects.filter(id=review_data['author']).first()
                if not title or not author:
                    self.stdout.write(self.style.WARNING(
                        "Не найдено произведение или автор"
                        f" для отзыва id={review_data['id']}"
                    ))
                    continue

                Review.objects.update_or_create(
                    id=review_data['id'],
                    defaults={
                        'title': title,
                        'text': review_data['text'],
                        'author': author,
                        'score': review_data['score'],
                        'pub_date': review_data['pub_date'],
                    }
                )
                count += 1

        self.stdout.write(f'Импортировано {count} отзывов из {path}')
        return True

    def import_comments(self, path):
        if not os.path.exists(path):
            self.stdout.write(self.style.ERROR(f'Файл {path} не найден.'))
            return False

        count = 0
        with open(path, encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for comment_data in reader:
                review = Review.objects.filter(
                    id=comment_data['review_id']).first()
                author = User.objects.filter(id=comment_data['author']).first()
                if not review or not author:
                    self.stdout.write(self.style.WARNING(
                        "Не найден отзыв или автор"
                        f" для комментария id={comment_data['id']}"
                    ))
                    continue

                Comment.objects.update_or_create(
                    id=comment_data['id'],
                    defaults={
                        'review': review,
                        'text': comment_data['text'],
                        'author': author,
                        'pub_date': comment_data['pub_date'],
                    }
                )
                count += 1
        self.stdout.write(f'Импортировано {count} комментариев из {path}')
        return True
