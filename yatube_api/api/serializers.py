"""Missing docstring."""
from posts.models import Comment, Group, Post
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField


class PostSerializer(serializers.ModelSerializer):
    """Missing docstring."""

    group = serializers.PrimaryKeyRelatedField(
        required=False,
        queryset=Group.objects.all()
    )
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        """Meta-data for posts serialize."""

        fields = ('id', 'text', 'author', 'image', 'group', 'pub_date')
        read_only_fields = ('author', 'group')
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    """Missing docstring."""

    post = serializers.PrimaryKeyRelatedField(read_only=True)
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        """Meta-data for comments serialize."""

        fields = ('id', 'author', 'post', 'text', 'created')
        model = Comment


class GroupSerializer(serializers.ModelSerializer):
    """Missing docstring."""

    class Meta:
        """Meta-data for group serialize."""

        fields = '__all__'
        model = Group
