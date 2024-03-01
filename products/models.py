from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Product(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='products'
    )
    name = models.CharField(
        'Название',
        max_length=200
    )
    date = models.DateTimeField(
        'Дата и время старта'
    )
    price = models.FloatField(
        'Стоимость',
        validators=(
            MinValueValidator(
                0,
                message='Значение не может быть отрицательным'
            ),
        )
    )
    min_count_students = models.PositiveIntegerField(
        'Минимальное количество студентов в группе'
    )
    max_count_students = models.PositiveIntegerField(
        'Максимальное количество студентов в группе'
    )

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name


class Access(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Продукт',
        related_name='access_product'
    )
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Студент',
        related_name='access_students'
    )
    access = models.BooleanField(
        'Доступ студента к продукту',
        default=False
    )

    class Meta:
        verbose_name = 'доступ студента к продукту'
        verbose_name_plural = 'Доступ студента к продукту'
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'student'],
                name='unique_product_student'
            )
        ]


class Lesson(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Продукт',
        related_name='lessons'
    )
    name = models.CharField(
        'Название',
        max_length=200
    )
    video_url = models.URLField(
        'Ссылка на видео',
        max_length=200
    )

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'Уроки'

    def __str__(self):
        return self.name


class Group(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Продукт',
        related_name='groups'
    )
    students = models.ManyToManyField(
        User,
        verbose_name='Студенты',
        related_name='groups_students'
    )
    name = models.CharField(
        'Название',
        max_length=200
    )
    affiliation = models.BooleanField(
        'Принадлежность группы к продукту'
    )

    class Meta:
        verbose_name = 'группа'
        verbose_name_plural = 'Группы'
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'name'],
                name='unique_product_group'
            )
        ]

    def __str__(self):
        return f'{self.product.name} - {self.name}'
