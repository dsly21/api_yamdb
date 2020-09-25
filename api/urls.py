from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ReviewsViewSet, CommentsViewSet

router = DefaultRouter()


router.register('reviews', ReviewsViewSet)
#router.register('comments', CommentsViewSet)


urlpatterns = [
    path('v1/', include(router.urls)),
]
