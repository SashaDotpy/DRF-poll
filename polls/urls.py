from django.contrib import admin
from django.urls import path, include
from rest_framework_nested import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from api.views import (
    PollViewSet,
    UserViewSet,
    AnswerViewSet,
    OptionViewSet,
    QuestionViewSet,
    PollWithUserAnswersViewSet,
)

router = routers.DefaultRouter()
router.register(r'polls', PollViewSet, basename='polls')
router.register(r'users', UserViewSet, basename='users')
router.register(r'questions', QuestionViewSet, basename='questions')
router.register(r'options', OptionViewSet, basename='options')
router.register(r'answers', AnswerViewSet, basename='answers')

users_router = routers.NestedSimpleRouter(router, r'users', lookup='user')
users_router.register(r'polls', PollWithUserAnswersViewSet, basename='polls')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(users_router.urls)),
    path('admin/', admin.site.urls),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
