from .models import Group


def get_list_students(groups):
    list_students = []
    for group in groups:
        list_students += group.students.all()
    return list_students


def get_new_group(product, count_groups):
    return Group.objects.create(
        name=f'{product.name}_{count_groups + 1}',
        affiliation=True,
        product=product)
