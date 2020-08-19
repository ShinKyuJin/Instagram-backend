from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from ssg.serializers import CreatePostSerializer, CommentSerializer, CreateCommentSerializer
from .serializers import UserSerializer, PostSerializer
from .models import User, Post, Comment


# users
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# posts
class PostListView(APIView):

    def get(self, request, format=None):
        instance = Post.objects.prefetch_related('comment_set').all().order_by('-id')
        serializer = PostSerializer(instance, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        print(request.data)
        serializer = CreatePostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


# 1 post
class PostDetailView(APIView):

    def get(self, request, pk, format=None):
        try:
            instance = Post.objects.prefetch_related('comment_set').get(pk=pk)
        except Exception as e:
            return Response({'message': str(e)}, status.HTTP_404_NOT_FOUND)
        serializer = PostSerializer(instance)
        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        try:
            instance = Post.objects.get(pk=pk)
        except Exception as e:
            return Response({'message': str(e)}, status.HTTP_404_NOT_FOUND)
        instance.delete()
        return Response({'message': 'deleted'}, status.HTTP_202_ACCEPTED)


# comments
class CommentListView(APIView):

    def get(self, request, pk, format=None):
        try:
            instance = Comment.objects.prefetch_related('post').filter(post=pk)
        except Exception as e:
            return Response({'message': str(e)}, status.HTTP_404_NOT_FOUND)
        serializer = CommentSerializer(instance, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request, pk, format=None):
        serializer = CreateCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class CommentDetailView(APIView):

    def get(self, request, pk_post, pk_comment, format=None):
        try:
            instance = Comment.objects.get(pk=pk_comment)
        except Exception as e:
            return Response({'message': str(e)}, status.HTTP_404_NOT_FOUND)
        serializer = CommentSerializer(instance)
        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, request, pk_post, pk_comment, format=None):
        try:
            instance = Comment.objects.get(pk=pk_comment)
        except Exception as e:
            return Response({'message': str(e)}, status.HTTP_404_NOT_FOUND)
        instance.delete()
        return Response({'message': 'deleted'}, status.HTTP_202_ACCEPTED)
