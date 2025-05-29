from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from reviews.constants import MIN_RATING, MAX_RATING


User = get_user_model()

class Title(models.Model):
    """Модель произведения."""

    name = models.TextField(null=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    """Модель отзывы."""

    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE)
    author = models.ForeignKey(
        User,
        verbose_name='Ревьюер',
        on_delete=models.CASCADE)
    text = models.TextField(
        verbose_name = 'Отзыв'
    )
    score = models.SmallIntegerField(
        verbose_name='Рейтинг',
        validators = [
            MinValueValidator(MIN_RATING), MaxValueValidator(MAX_RATING)
        ]
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        default_related_name = 'reviews'
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            )
        ]

    def __str__(self):
        return (
            f'Отзыв от {self.author} '
            f'на произведение {self.title.name}.'
        )


class Comment(models.Model):
    """Модель комментарии."""

    review = models.ForeignKey(
        Review,
        verbose_name='Комментарий',
        on_delete=models.CASCADE)
    author = models.ForeignKey(
        User,
        verbose_name='Комментатор',
        on_delete=models.CASCADE)
    text = models.TextField()
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'
        ordering = ['-pub_date']
 
    def __str__(self):
        return (
            f'Комментарий от {self.author} '
            f'на отзыв {self.review.author} '
            f'к произведению {self.review.title.name}.'
        )
