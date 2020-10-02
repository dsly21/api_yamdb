from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

router = DefaultRouter()


# router.register('reviews', views.ReviewsViewSet)
router.register('titles', views.TitleView)
router.register('categories', views.CategoryView)
router.register('genres', views.GenreView)
router.register(r'titles/(?P<titles_id>\d+)/reviews',
                views.ReviewsViewSet, basename="reviews")
router.register(
                r'titles/(?P<titles_id>\d+)/reviews/(?P<reviews_id>\d+)/comments',
                views.CommentsViewSet,
                basename='comments')


urlpatterns = [
    path('v1/', include(router.urls)),
    path(
        'v1/auth/token/',
        views.TokenGetView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'v1/auth/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
    path('v1/auth/email/', views.send_email),
]
