from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import (
    PageNumberPagination,
    LimitOffsetPagination
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from posts.models import Follow, Group, Post, User
from .permissions import OwnerOrReadOnly
from .serializers import (
    CommentSerializer,
    FollowSerializer,
    PostSerializer,
    GroupSerializer
)


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


class FollowApi(APIView):
    permission_classes = [IsAuthenticated]
    filter_backends = (filters.SearchFilter, )
    search_fields = ('following__username', )

    def get(self, request, format=None):
        follows = Follow.objects.filter(user=request.user)
        search = request.query_params.get('search', None)
        if search:
            follows = follows.filter(following__username__icontains=search)
        serializer = FollowSerializer(follows, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        following_username = request.data.get('following')
        if not following_username:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        following = get_object_or_404(User, username=following_username)

        # Проверяем была ли ранее подписка на этого же пользователя.
        if Follow.objects.filter(
            user=request.user, following=following
        ).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # Проверяем подписывается ли пользователь на самого себя.
        if request.user == following:
            raise ValidationError(
                'Пользователь не может подписаться на самого себя.'
            )

        follow = Follow(user=request.user, following=following)
        follow.save()

        serializer = FollowSerializer(follow)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
