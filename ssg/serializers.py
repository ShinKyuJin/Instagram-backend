from rest_framework import serializers

from .models import User, Post, Comment


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'user_avatar']


class CommentSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = Comment
        fields = ['id', 'author', 'content', 'created_at']


class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['author', 'post', 'content']

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)



class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    comments = CommentSerializer(source='comment_set', many=True)

    class Meta:
        model = Post
        fields = ['id', 'author', 'comments', 'title', 'picture', 'created_at']


class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['author', 'title', 'picture']

    def create(self, validated_data):
        return Post.objects.create(**validated_data)
