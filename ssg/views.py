from rest_framework import viewsets
from .serializers import UserSerializer, PostSerializer
from .models import User, Post


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-id')
    serializer_class = PostSerializer

# Create your views here.
