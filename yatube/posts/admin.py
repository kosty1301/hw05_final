from django.contrib import admin
from django.conf import settings as conf_settings

from .models import Group, Post, Comment, Follow


EMPTY_VALUE_DISPLAY = conf_settings.EMPTY_VALUE_DISPLAY


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Посты."""
    list_display = ('pk', 'text', 'pub_date', 'author', 'group',)
    list_editable = ('group',)
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    """Группы, связь с постами один ко многим."""
    list_display = ('title', 'slug', 'description',)
    search_fields = ('title',)
    list_filter = ('slug',)
    empty_value_display = EMPTY_VALUE_DISPLAY


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Комментарии"""
    list_display = ('post', 'author', 'text',)
    search_fields = ('author',)
    list_filter = ('post',)


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """Комментарии"""
    list_display = ('user', 'author',)
    search_fields = ('author',)
    list_filter = ('user',)
