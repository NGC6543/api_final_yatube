from django.urls import include, path
from rest_framework import routers

from .views import PostViewSet, GroupViewSet, CommentViewSet, FollowViewSet

router_v1 = routers.SimpleRouter()
router_v1.register('posts', PostViewSet, basename='posts')
router_v1.register('groups', GroupViewSet, basename='groups')
router_v1.register(
    r'posts/(?P<post_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
router_v1.register('follow', FollowViewSet, basename='follows')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/', include('djoser.urls.jwt')),
]
