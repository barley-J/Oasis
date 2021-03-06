from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

from common.utils import get_time_filename
from common.models import Base


def get_video_path(instance, filename):
    return 'video/{}'.format(get_time_filename(filename))


# 帖子
class Post(Base):
    # 用户
    user = models.ForeignKey('user.User',
                             related_name='post_user',
                             on_delete=models.CASCADE,
                             verbose_name=u'用户')
    # 状态
    STATUS = {
        0: u'公开',
        1: u'好友可见',
        2: u'仅我可见',
    }
    status = models.PositiveIntegerField(choices=STATUS.items(),
                                         default=0,
                                         verbose_name=u'状态')
    # 标题
    title = models.CharField(max_length=100,
                             verbose_name=u'标题')
    # 详情
    content = models.TextField(null=True,
                               verbose_name=u'详情')
    # 类型
    CATEGORY = {
        0: u'视频',
        1: u'图片',
    }
    category = models.PositiveIntegerField(choices=CATEGORY.items(),
                                           verbose_name=u'类型')
    # 视频
    video = models.ForeignKey('user.File',
                              related_name='post_video',
                              null=True,
                              blank=True,
                              verbose_name=u'视频')
    # 图片
    images = models.ManyToManyField('user.File',
                                    blank=True,
                                    verbose_name='图片')
    # 时间
    time = models.DateTimeField(null=True,
                                default=timezone.now,
                                verbose_name='时间')
    # 地点-名称
    place = models.CharField(max_length=255,
                             null=True,
                             blank=True,
                             verbose_name='地点-名称')
    # 地点-经度
    longitude = models.DecimalField(null=True,
                                    blank=True,
                                    max_digits=9,
                                    decimal_places=6,
                                    validators=[MinValueValidator(-180), MaxValueValidator(180)],
                                    verbose_name=u'地点-经度')
    # 地点-纬度
    latitude = models.DecimalField(null=True,
                                   blank=True,
                                   max_digits=8,
                                   decimal_places=6,
                                   validators=[MinValueValidator(-90), MaxValueValidator(90)],
                                   verbose_name=u'地点-纬度')
    # 点赞用户
    likes = models.ManyToManyField('user.User',
                                   blank=True,
                                   verbose_name='点赞用户')

    class Meta:
        verbose_name = '帖子'
        verbose_name_plural = '帖子'

    # 点赞总数
    def get_likes_count(self):
        return self.likes.count()

    # 评论总数
    def get_comment_count(self):
        return Comment.objects.filter(post=self).count()

    def __str__(self):
        return '{} {}'.format(self.id, self.title)


# 评论
class Comment(Base):
    # 用户
    user = models.ForeignKey('user.User',
                             related_name='comment_user',
                             verbose_name=u'用户')
    # 帖子
    post = models.ForeignKey('post.Post',
                             related_name='comment_post',
                             verbose_name=u'帖子')
    # 评论内容
    text = models.TextField(verbose_name=u'评论内容')
    # 父评论
    parent = models.ForeignKey('self',
                               null=True,
                               blank=True,
                               verbose_name=u'父评论')
    # 点赞用户
    likes = models.ManyToManyField('user.User',
                                   blank=True,
                                   verbose_name='点赞用户')

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = '评论'

    def clean(self):
        if self.parent and self.parent.post != self.post:
            raise ValidationError({'parent': '父评论所属帖子必须与本评论所属帖子一致'})

    # 点赞总数
    def get_likes_count(self):
        return self.likes.count()

    def __str__(self):
        return '{} {} {}'.format(self.id, self.user, self.post)
