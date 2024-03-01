from datetime import datetime

from django.contrib.auth import get_user_model
from django.db.models import Count
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Access, Product
from .utils import get_list_students, get_new_group

User = get_user_model()


@receiver(post_save, sender=User)
def create_access_student(sender, instance, created, **kxargs):
    products = Product.objects.all()
    if created:
        Access.objects.bulk_create(
            Access(product=product, student=instance)
            for product in products
        )


@receiver(post_save, sender=Product)
def create_access_student(sender, instance, created, **kxargs):
    users = User.objects.all()
    if created:
        Access.objects.bulk_create(
            Access(product=instance, student=user)
            for user in users
        )


@receiver(post_save, sender=Access)
def create_access_student(sender, instance, **kxargs):
    if instance.access:
        product = instance.product
        student = instance.student
        groups = product.groups.all()
        count_groups = len(groups)
        count_students = groups.aggregate(Count('students'))['students__count']
        list_students = get_list_students(groups)
        if (count_groups > 0
                and product.date.timestamp() < datetime.now().timestamp()
                and count_students / count_groups != product.max_count_students
                and student not in list_students):
            for group in groups:
                if group.students.count() < product.max_count_students:
                    group.students.add(student)
        elif (count_groups > 0
                and product.date.timestamp() < datetime.now().timestamp()
                and count_students / count_groups == product.max_count_students
                and student not in list_students):
            new_group = get_new_group(product, count_groups)
            new_group.students.add(student)
        elif (count_groups > 0
                and product.date.timestamp() > datetime.now().timestamp()
                and count_students / count_groups == product.max_count_students
                and student not in list_students):
            get_new_group(product, count_groups)
            groups = product.groups.all()
            list_students.append(student)
            if (len(list_students) / (count_groups + 1)
                    >= product.min_count_students):
                end = (count_students + 1) // (count_groups + 1)
                count = len(list_students) % (count_groups + 1)
                for i in range(count_groups + 1):
                    groups[i].students.clear()
                    if i < count:
                        groups[i].students.set(list_students[0:end + 1])
                        list_students = list_students[end + 1:]
                    else:
                        groups[i].students.set(list_students[0:end])
                        list_students = list_students[end:]
            else:
                end = product.min_count_students
                count = len(list_students) // (product.min_count_students)
                for i in range(count_groups + 1):
                    groups[i].students.clear()
                    if i < count:
                        groups[i].students.set(list_students[0:end])
                        list_students = list_students[end:]
                    else:
                        groups[i].students.set(list_students)
        elif (count_groups > 0
                and product.date.timestamp() > datetime.now().timestamp()
                and count_students / count_groups != product.max_count_students
                and student not in list_students):
            if (count_students % count_groups == 0
                    and count_students / count_groups
                    >= product.min_count_students):
                groups[0].students.add(student)
            else:
                for group in groups:
                    if group.students.count() < count_students / count_groups:
                        group.students.add(student)
                        break
        elif (count_groups == 0):
            new_group = get_new_group(product, count_groups)
            new_group.students.add(student)
