from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status, viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from ssg.serializers import CreatePostSerializer, CommentSerializer, CreateCommentSerializer
from .serializers import UserSerializer, PostSerializer
from .models import User, Post, Comment


# users
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# posts
class PostListView(APIView):

    def get(self, request):
        posts = Post.objects.all().order_by('-created_at')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CreatePostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


# 1 post
class PostDetailView(APIView):

    def get(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Exception as e:
            return Response({'message': str(e)}, status.HTTP_404_NOT_FOUND)
        serializer = PostSerializer(post)
        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response({'message': '게시물을 찾을 수 없습니다.'}, status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': ''}, status.HTTP_500_INTERNAL_SERVER_ERROR)
        try:
            deleted: Post = post.delete()
        except ObjectDoesNotExist:
            return Response({'message': '게시물이 이미 삭제되었습니다.'}, status.HTTP_208_ALREADY_REPORTED)
        return Response(deleted, status.HTTP_202_ACCEPTED)


# comments
class CommentListView(APIView):

    def get(self, request, pk):
        try:
            comments = Comment.objects.filter(post=pk)
        except Exception as e:
            return Response({'message': str(e)}, status.HTTP_404_NOT_FOUND)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request, pk):
        serializer = CreateCommentSerializer(data=request.data)
        if serializer.is_valid():
            created: Comment = serializer.save()
            serialized_created = CommentSerializer(instance=created)
            return Response(serialized_created.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class CommentDetailView(APIView):

    def get(self, request, pk_post, pk_comment):
        try:
            comment = Comment.objects.get(pk=pk_comment)
        except Exception as e:
            return Response({'message': str(e)}, status.HTTP_404_NOT_FOUND)
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, request, pk_post, pk_comment):
        try:
            comment = Comment.objects.get(pk=pk_comment)
        except Exception as e:
            return Response({'message': str(e)}, status.HTTP_404_NOT_FOUND)
        try:
            deleted: Comment = comment.delete()
        except Exception as e:
            return Response({'message': '이미 삭제되었습니다.'}, status.HTTP_208_ALREADY_REPORTED)
        return Response(deleted, status.HTTP_202_ACCEPTED)
