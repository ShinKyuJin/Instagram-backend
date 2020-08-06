from rest_framework import viewsets
from .serializers import UserSerializer, PostSerializer
from .models import User, Post

from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def login(request):
    if 'X-login-userid' in request.headers:
        is_user_in = User.objects.filter(user_id=request.headers['X-login-userid'], user_password=request.headers['X-login-userpw'])
        if is_user_in:
            return Response({"message": 'hello'})
    
    return Response({"message": 'No Way'})

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-id')
    serializer_class = PostSerializer
