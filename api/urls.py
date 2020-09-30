from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

router = DefaultRouter()


router.register('reviews', views.ReviewsViewSet)
#router.register('comments', views.CommentsViewSet)


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/token/', views.TokenGetView.as_view(),
         name='token_obtain_pair'),
    path('v1/auth/token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
    path('v1/auth/email/', views.send_email),
    path('v1/users/', views.UsersViewSet.as_view())
]
