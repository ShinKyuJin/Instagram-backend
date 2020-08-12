from rest_framework import viewsets
from .serializers import UserSerializer, PostSerializer, CommentSerializer
from .models import User, Post, Comment

from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET']) # /login/
def login(request):
    if 'X-login-userid' in request.headers:
        is_user_in = User.objects.get(user_id=request.headers['X-login-userid'],
                                      user_password=request.headers['X-login-userpw'])
        if is_user_in:
            return Response({"message": is_user_in.id})
        else:
            return Response({"message": "No Way"})

    return Response({"message": 'No Way'})


@api_view(['GET', 'POST']) # /user/
def users(request):
    instance = User.objects.all()

    if request.method == 'GET':
        serializer = UserSerializer(instance, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)

        try:
            serializer.is_valid()
            created: User = serializer.create(serializer.validated_data)
            return Response({"response": "created"})
        except Exception:
            return Response({"123": "Exception"})


@api_view(['GET', 'DELETE', 'PUT']) # /user/{pk}/
def user(request, pk):
    try:
        instance = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({"message": "없는 유저입니다."})

    if request.method == 'GET':
        serializer = UserSerializer(instance)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        instance.delete()
        return Response({"message": "삭제되었습니다."})

    elif request.method == 'PUT':
        serializer = UserSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({'message': '제대로 수정되지 않았습니다.'})


@api_view(['GET', 'POST']) # /post/
def posts(request):
    instance = Post.objects.all().order_by('-id')
    serializer = PostSerializer(instance, many=True)
    if request.method == 'GET':
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PostSerializer(data=request.data)

        try:
            serializer.is_valid()
            created: Post = serializer.create(serializer.validated_data)
            return Response({"response": str(created)})
        except Exception as e:
            return Response({"123": str(e)})


@api_view(['GET', 'PUT', 'DELETE']) # /post/{pk}/
def post(request, pk):
    try:
        instance = Post.objects.get(pk=pk)
    except Exception as e:
        return Response({"error": str(e)})

    if request.method == 'GET':
        serializer = PostSerializer(instance)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        try:
            instance.delete()
        except Exception as e:
            return Response({'message': str(e)})
        return Response({"message": "글이 삭제되었습니다."})
    elif request.method == 'PUT':
        serializer = PostSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({'message': '수정에 실패했습니다.'})


@api_view(['GET', 'POST']) # /post/{pk}/comment/
def comments(request, pk):
    try:
        post_id = Post.objects.get(pk=pk)
        instance = Comment.objects.filter(post=post_id)
    except Exception as e:
        return Response({'message': str(e)})
    serializer = CommentSerializer(instance, many=True)
    if request.method == 'GET':
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        try:
            serializer.is_valid()
            created: Comment = serializer.create(serializer.validated_data)
            return Response({"response": str(created)})
        except Exception as e:
            return Response({"message": str(e)})


@api_view(['GET', 'DELETE', 'PUT'])
def comment(request, post_pk, comment_pk): # /post/{any}/comment/{comment_pk}
    try:
        instance = Comment.objects.get(pk=comment_pk)
    except Exception as e:
        return Response({'msg': str(e)})
    if request.method == 'GET':
        serializer = CommentSerializer(instance)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        try:
            instance.delete()
        except Exception as e:
            return Response({'message': str(e)})
        return Response({"message": "댓글이 삭제되었습니다."})
    elif request.method == 'PUT':
        serializer = CommentSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({'message': '댓글 수정에 실패했습니다.'})


@api_view(['GET'])
def user_me(request):
    if request.method == 'GET':
        if 'X-id' in request.headers:
            try:
                user_instance = User.objects.get(pk=request.headers['X-id'])
                user_serializer = UserSerializer(instance=user_instance)
            except Exception as e:
                return Response({'message': str(e)})
            try:
                post_instance = Post.objects.filter(author=request.headers['X-id']).order_by('-id')
                post_serializer = PostSerializer(instance=post_instance, many=True)
            except Exception as e:
                return Response({'message': str(e)})

            return Response({'user': user_serializer.data, 'post': post_serializer.data})
        return Response({'message': '로그인이 필요한 작업입니다.'})
