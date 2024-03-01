from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from products.models import Access, Product

from .serializers import (LessonSerializer, ProductSerializer,
                          StatisticProductSerializer)


class ProductViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class LessonViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        product = get_object_or_404(
            Product,
            pk=self.kwargs['product_id']
        )
        access = get_object_or_404(
            Access,
            product=product,
            student=self.request.user
        )
        if access.access:
            return product.lessons.all()


class StatisticProductViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = StatisticProductSerializer
