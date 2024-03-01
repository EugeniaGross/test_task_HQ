from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import LessonViewSet, ProductViewSet, StatisticProductViewSet

router = SimpleRouter()
router.register(
    'products',
    ProductViewSet,
    basename='products'
)
router.register(
    r'products/(?P<product_id>\d+)/lessons',
    LessonViewSet,
    basename='lessons'
)
router.register(
    'products_statistic',
    StatisticProductViewSet,
    basename='products_statistic'
)

urlpatterns = [
    path('', include(router.urls)),
]
