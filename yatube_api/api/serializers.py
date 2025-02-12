from rest_framework import serializers
from rest_framework.relations import SlugRelatedField


from posts.models import Comment, Follow, Group, Post, User


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'text', 'pub_date', 'author', 'group', 'image')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'author', 'text', 'created', 'post')
        read_only_fields = ('post', )


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')


# class FollowSerializer(serializers.ModelSerializer):
#     user = SlugRelatedField(slug_field='username', read_only=True)
#     # following = SlugRelatedField(slug_field='username')
#     following = serializers.SerializerMethodField(read_only=True)

#     class Meta:
#         model = Follow
#         fields = ('user', 'following')
#         # read_only_fields = ('following',)

#     # def get_user(self, obj):
#     #     return obj.user.username

#     def get_following(self, obj):
#         return obj.followers.username
    
    # def validate(self, data):
    #     print(data.get('user'))
    #     # Ensuring that both user and following are not None or empty
    #     # if not data.get('user'):
    #     #     raise serializers.ValidationError("User field is required.")
    #     if not data.get('following'):
    #         raise serializers.ValidationError("Following field is required.")
    #     return data


class FollowSerializer(serializers.ModelSerializer):
    user = SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    following = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = ('user', 'following')

    def get_following(self, obj):
        return obj.following.username
