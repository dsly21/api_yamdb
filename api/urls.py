from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

router = DefaultRouter()

router.register('titles', views.TitleView)
router.register('categories', views.CategoryView)
router.register('genres', views.GenreView)
router.register(r'titles/(?P<titles_id>\d+)/reviews',
                views.ReviewsViewSet, basename="reviews")
router.register(
    r'titles/(?P<titles_id>\d+)/'
    r'reviews/(?P<reviews_id>\d+)/comments',
    views.CommentsViewSet,
    basename='comments')
router.register('users', views.UsersViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/token/', views.get_token),
    # email и confirmation code передаются в теле запроса
    path('v1/auth/email/', views.send_email),
    # email передается в теле запроса
]
