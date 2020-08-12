from rest_framework import serializers
from .models import User, Post, Comment


class UserSerializer(serializers.BaseSerializer):

    def to_representation(self, instance):
        data = {
            'id': instance.id,
            'user_id': instance.user_id,
            'user_password': instance.user_password,
            'user_email': instance.user_email,
            'user_avatar': instance.user_avatar,
            'created_at': instance.created_at
        }
        return data

    def to_internal_value(self, data):
        user_id = data.get('user_id')
        user_password = data.get('user_password')
        user_email = data.get('user_email')
        user_avatar = data.get('user_avatar')
        
        return {
            'user_id': user_id,
            'user_password': user_password,
            'user_email': user_email,
            'user_avatar': user_avatar
        }
    
    def create(self, validated_data):
        return User.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.user_id = validated_data.get('user_id', instance.user_id)
        instance.user_password = validated_data.get('user_password', instance.user_password)
        instance.user_email = validated_data.get('user_email', instance.user_email)
        instance.user_avatar = validated_data.get('user_avatar', instance.user_avatar)
        instance.save()
        return instance
        

class PostSerializer(serializers.BaseSerializer):

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'author': {'user_id': instance.author.user_id, 'user_avatar': instance.author.user_avatar},
            'title': instance.title,
            'picture': 'http://localhost:8000' + instance.picture.url,
            'created_at': instance.created_at
        }

    def to_internal_value(self, data):
        author = data.get('author')
        title = data.get('title')
        picture = data.get('picture')

        return {
            'author': int(author),
            'title': title,
            'picture': picture
        }

    def create(self, validated_data):
        author = User.objects.get(pk=validated_data['author'])
        try:
            return Post.objects.create(
                author=author,
                title=validated_data['title'],
                picture=validated_data['picture'])
        except Exception as e:
            return {"error": str(e)}


class CommentSerializer(serializers.BaseSerializer):

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'author': {'id': instance.author.id, 'user_id': instance.author.id},
            'post': instance.post.id,
            'content': instance.content
        }

    def to_internal_value(self, data):
        author = int(data.get('author'))
        post = int(data.get('post'))
        content = data.get('content')

        return {
            'author': author,
            'post': post,
            'content': content,
        }

    def create(self, validated_data):
        author = User.objects.get(id=validated_data['author'])
        post = Post.objects.get(pk=validated_data['post'])
        try:
            return Comment.objects.create(
                author=author,
                post=post,
                content=validated_data['content'])
        except Exception as e:
            return {"error": str(e)}
