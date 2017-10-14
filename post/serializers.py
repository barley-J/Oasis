from common.serializers import *
from common.utils import get_time_filename, validate_image_size, validate_video_size, get_list
from user.serializers import UserListSerializer
from .models import *


# --------------------------------- 图片 ---------------------------------
# 创建图片
class ImageModifySerializer(ModelSerializer):
    class Meta:
        model = Image
        fields = ('user', 'image')


# 列表图片
class ImageListSerializer(ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'user', 'image', 'create_time')


# 图片详情
class ImageSerializer(ModelSerializer):
    user = UserListSerializer(read_only=True)

    class Meta:
        model = Image
        fields = ('id', 'user', 'image', 'create_time')


# --------------------------------- 帖子 ---------------------------------
# 创建帖子
class PostModifySerializer(ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(validators=[validate_image_size],
                                     allow_empty_file=False,
                                     use_url=False)
    )

    def validate(self, data):
        if self.instance is None:
            category = data['category']
        else:
            category = self.instance.category

        if category == 0:
            if 'images' in data and len(data['images']) != 0:
                raise ValidationError({'images': '视频不接收多图'})
            elif 'video' not in data:
                raise ValidationError({'video': '视频必传'})
        elif category == 1:
            if 'video' in data:
                raise ValidationError({'video': '多图不接收视频'})
            elif 'images' not in data or len(data['images']) == 0:
                raise ValidationError({'images': '多图必传'})
        return data

    def create(self, validated_data):
        print(validated_data)
        images = validated_data.pop('images')
        post = Post.objects.create(**validated_data)
        if post.category == 1:
            # 多图
            for image in images:
                post.images.add(Image.objects.create(user=post.user, image=image))
        return post

    # images新图片 images_delete待删除图片ID列表
    def update(self, instance, validated_data):
        print(validated_data)
        # 从validated_date移除images为setattr方法做准备
        if 'images' in validated_data:
            images = validated_data.pop('images')
        else:
            images = []

        if instance.category == 1:
            # 更新多图
            for image in images:
                instance.images.add(Image.objects.create(user=instance.user, image=image))
            for image_d in Image.objects.filter(id__in=get_list(self.context['request'].data, 'images_delete'),
                                                user=instance.user):
                instance.images.remove(image_d)

        # 更新实例
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    class Meta:
        model = Post
        fields = ('user', 'status', 'title', 'content', 'category', 'video', 'images', 'place', 'location')
        read_only_fields = ('user',)


# 列表帖子
class PostListSerializer(ModelSerializer):
    user = UserListSerializer(read_only=True)
    images = ImageListSerializer(read_only=True, many=True)

    def to_representation(self, instance):
        """视频只返回video 图片只返回images"""
        data = super(PostListSerializer, self).to_representation(instance)
        if instance.category == 0:
            data.pop('images', None)
        elif instance.category == 1:
            data.pop('video', None)
        return data

    class Meta:
        model = Post
        fields = ('id', 'user', 'status', 'title', 'content', 'category', 'video', 'images', 'time', 'place',
                  'location')


# 帖子详情
class PostSerializer(ModelSerializer):
    user = UserListSerializer(read_only=True)
    images = ImageListSerializer(read_only=True, many=True)

    def to_representation(self, instance):
        """视频只返回video 图片只返回images"""
        data = super(PostSerializer, self).to_representation(instance)
        if instance.category == 0:
            data.pop('images', None)
        elif instance.category == 1:
            data.pop('video', None)
        return data

    class Meta:
        model = Post
        fields = ('id', 'user', 'status', 'title', 'content', 'category', 'video', 'images', 'time', 'place',
                  'location', 'get_status_display', 'get_category_display')