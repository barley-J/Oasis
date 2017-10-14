import logging

from datetime import datetime
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from django.db.models import Q
from rest_framework.decorators import list_route
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.throttling import UserRateThrottle

from common.permissions import IsPostOwnerOrReadOnly
from common.response import success_response, error_response
from common.viewset import ModelViewSet, CreateModelMixin, HumanizationSerializerErrorsMixin, GenericViewSet
from common.exception import VerifyError

from friend.models import Friend

from .models import *
from .serializers import *
from .filters import *

logger = logging.getLogger("info")


# 帖子
class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    serializer_classes = {
        'create': PostModifySerializer,
        'list': PostListSerializer,
        'retrieve': PostSerializer,
        'update': PostModifySerializer,
    }
    permission_classes = (IsAuthenticated,)
    filter_class = PostFilter
    ordering_fields = '__all__'
    search_fields = ('title', 'content', 'user__nickname')

    # 修改、删除需要所有者权限
    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'destroy'):
            self.permission_classes = [IsAuthenticated, IsPostOwnerOrReadOnly, ]
        return super(self.__class__, self).get_permissions()

    # 帖子所有者是自己
    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    # 假删除
    def perform_destroy(self, instance):
        instance.is_abandon = True
        instance.save()

    # 我的帖子列表
    def list(self, request, *args, **kwargs):
        queryset = self.queryset.filter(user=request.user)
        return self.list_queryset(request, queryset, *args, **kwargs)

    # 故事列表
    @list_route(methods=['GET'])
    def story_list(self, request, *args, **kwargs):
        my_friends = [friend.to_user for friend in Friend.objects.filter(from_user=request.user, is_block=False).all()]
        queryset = self.queryset.filter(user__in=my_friends, status=1).all()
        return self.list_queryset(request, queryset, *args, **kwargs)

    # 帖子列表
    @list_route(methods=['GET'])
    def post_list(self, request, *args, **kwargs):
        queryset = self.queryset.filter(status=0).all()
        return self.list_queryset(request, queryset, *args, **kwargs)
