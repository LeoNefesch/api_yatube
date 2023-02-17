"""Missing docstring."""
from django.shortcuts import get_object_or_404
from posts.models import Group, Post
from rest_framework import status, viewsets
from rest_framework.exceptions import PermissionDenied

from .serializers import CommentSerializer, GroupSerializer, PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    """Redefinition of DELETE-method."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        """Redefinition of POST-method."""
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        """Redefinition of PUT-method."""
        if serializer.instance.author != self.request.user:
            raise PermissionDenied(
                'Изменение чужого контента запрещено!',
            )
        super(PostViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        """Redefinition of DELETE-method."""
        if instance.author != self.request.user:
            raise PermissionDenied(
                'Объект не найден!',
            )
        super(PostViewSet, self).perform_destroy(instance)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Missing docstring."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """Missing docstring."""

    serializer_class = CommentSerializer

    def get_queryset(self):
        """Redefinition of GET-method."""
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        return post.comments.all()

    def perform_create(self, serializer):
        """Redefinition of POST-method."""
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        serializer.save(author=self.request.user, post=post)

    def perform_update(self, serializer):
        """Redefinition of PUT-method."""
        if serializer.instance.author != self.request.user:
            raise PermissionDenied(
                'Изменение чужого контента запрещено!',
                status.HTTP_403_FORBIDDEN
            )
        super(CommentViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        """Missing docstring."""
        if instance.author != self.request.user:
            raise PermissionDenied(
                'Нет комментария для удаления!',
            )
        super(CommentViewSet, self).perform_destroy(instance)
