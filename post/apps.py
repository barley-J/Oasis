from django.apps import AppConfig


class PostConfig(AppConfig):
    name = 'post'
    verbose_name = '帖子'

    def ready(self):
        import post.signals
