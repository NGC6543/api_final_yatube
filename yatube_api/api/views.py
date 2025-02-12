from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from posts.models import Follow, Post, Group, User
from .permissions import OnlyAuthorHasPermissions, OwnerOrReadOnly, CanSeeFollow
from .serializers import CommentSerializer, FollowSerializer, PostSerializer, GroupSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (OwnerOrReadOnly, )
    pagination_class = PageNumberPagination
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    # permission_classes = (IsAuthenticated, OnlyAuthorHasPermissions, )
    permission_classes = (OwnerOrReadOnly, )

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        serializer.save(author=self.request.user, post=post)

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        return post.comments.all()


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (OwnerOrReadOnly, )


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated, )
    filter_backends = (filters.SearchFilter, )
    search_fields = ('following__username', )

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        user = self.request.user
        following_username = self.request.data.get('following')

        # following = get_object_or_404(User, username=following_username)
        try:
            following = User.objects.get(username=following_username)
        except User.DoesNotExist:
            raise ValidationError(
                {"detail": "The user to follow does not exist."}
            )

        if user == following:
            raise ValidationError(
                {"detail": "A user cannot follow themselves."}
            )

        if Follow.objects.filter(user=user, following=following).exists():
            raise ValidationError({"detail": "You are already following this user."})
        serializer.save(user=user, following=following)
