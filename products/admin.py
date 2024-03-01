from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Access, Group, Lesson, Product

User = get_user_model()


@admin.register(Access)
class AccessAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'student',
        'access'
    )


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'name',
        'video_url'
    )


@admin.register(Group)
class Group(admin.ModelAdmin):
    list_display = (
        'product',
        'name',
        'affiliation'
    )
    filter_horizontal = ('students', )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'name',
        'date',
        'price',
        'min_count_students',
        'max_count_students'
    )
