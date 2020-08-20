"""inssgtagram URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path

from django.conf.urls import include

from ssg import views

from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('user/', views.UserViewSet.as_view({"get": "list", "post": "create"})),
    path('user/<int:pk>/', views.UserViewSet.as_view({"get": "retrieve", "delete": "destroy"})),

    path('post/', views.PostListView.as_view()),
    path('post/<int:pk>/', views.PostDetailView.as_view()),
    path('post/<int:pk>/comment/', views.CommentListView.as_view()),
    path('post/<int:pk_post>/comment/<int:pk_comment>/', views.CommentDetailView.as_view()),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls))
    ] + urlpatterns
