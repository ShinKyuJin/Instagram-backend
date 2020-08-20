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
    authentication_classes = (BasicAuthentication, JWTAuthentication)
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        posts = Post.objects.prefetch_related('comment_set').all().order_by('-id')
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
            post = Post.objects.prefetch_related('comment_set').get(pk=pk)
        except Exception as e:
            return Response({'message': str(e)}, status.HTTP_404_NOT_FOUND)
        serializer = PostSerializer(post)
        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            instance = Post.objects.get(pk=pk)
        except Exception as e:
            return Response({'message': str(e)}, status.HTTP_404_NOT_FOUND)
        instance.delete()
        return Response({'message': 'deleted'}, status.HTTP_202_ACCEPTED)


# comments
class CommentListView(APIView):

    def get(self, request, pk):
        try:
            instance = Comment.objects.prefetch_related('post').filter(post=pk)
        except Exception as e:
            return Response({'message': str(e)}, status.HTTP_404_NOT_FOUND)
        serializer = CommentSerializer(instance, many=True)
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
            instance = Comment.objects.get(pk=pk_comment)
        except Exception as e:
            return Response({'message': str(e)}, status.HTTP_404_NOT_FOUND)
        serializer = CommentSerializer(instance)
        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, request, pk_post, pk_comment):
        try:
            instance = Comment.objects.get(pk=pk_comment)
        except Exception as e:
            return Response({'message': str(e)}, status.HTTP_404_NOT_FOUND)
        instance.delete()
        return Response({'message': 'deleted'}, status.HTTP_202_ACCEPTED)
