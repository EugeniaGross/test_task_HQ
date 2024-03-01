from django.contrib.auth import get_user_model
from django.db.models import Count
from rest_framework import serializers

from products.models import Lesson, Product

User = get_user_model()


class ProductSerializer(serializers.ModelSerializer):
    count_lessons = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'author',
            'name',
            'date',
            'price',
            'count_lessons'
        )

    def get_count_lessons(self, obj):
        return obj.lessons.count()


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = (
            'name',
            'video_url'
        )


class StatisticProductSerializer(serializers.ModelSerializer):
    count_students = serializers.SerializerMethodField()
    fullness_of_groups = serializers.SerializerMethodField()
    purchase_percentage = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'author',
            'name',
            'date',
            'price',
            'count_students',
            'fullness_of_groups',
            'purchase_percentage'
        )

    def get_count_students(self, obj):
        return obj.groups.all().aggregate(
            Count('students')
        )['students__count']

    def get_fullness_of_groups(self, obj):
        count_groups = obj.groups.count()
        count_students = obj.groups.all().aggregate(
            Count('students')
        )['students__count']
        fullness = count_students / count_groups / obj.max_count_students
        return f'{fullness * 100} %'

    def get_purchase_percentage(self, obj):
        count_users = User.objects.count()
        count_students = obj.groups.all().aggregate(
            Count('students')
        )['students__count']
        return f'{count_students / count_users * 100} %'
