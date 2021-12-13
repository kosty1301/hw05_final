from django.apps import AppConfig


class PostsConfig(AppConfig):
    """Отображение в админке постов."""
    name = 'posts'
    verbose_name = 'Посты'


class GroupConfig(AppConfig):
    """Отображение в админке групп."""
    name = 'group'
    verbose_name = 'группы'
