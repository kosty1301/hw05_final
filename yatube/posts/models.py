from django.db import models
from django.contrib.auth import get_user_model
from core.models import CreatedModel
from django.db.models import Q

User = get_user_model()
AUTHOR_HELP_TEXT = 'Автор'


class Group(models.Model):
    """Группы, связь с постами один ко многим."""
    title = models.CharField(
        'заголовок',
        max_length=200,
        help_text='Название группы'
    )
    slug = models.SlugField(
        'обозначение',
        unique=True,
        help_text='сокр. название'
    )
    description = models.TextField(
        'описание',
        null=True,
        blank=True,
        help_text='Описание'
    )

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return self.title


class Post(models.Model):
    """Посты."""
    text = models.TextField(
        'тест',
        max_length=400,
        help_text='Текст поста'
    )
    pub_date = models.DateTimeField(
        'дата публикации',
        auto_now_add=True,
        help_text='Дата публикации'
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        related_name='group',
        blank=True, null=True,
        help_text='Группа'
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        help_text=AUTHOR_HELP_TEXT
    )
    image = models.ImageField(
        'Картинка',
        upload_to='posts/',
        blank=True,
        help_text='Картинка'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.text[:15]


class Comment(CreatedModel):
    """Комментарии."""
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        help_text='Пост'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        help_text=AUTHOR_HELP_TEXT
    )
    text = models.TextField('тест', max_length=400,
                            help_text='Текст нового комментария')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        help_text='Пользователь'
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        help_text=AUTHOR_HELP_TEXT
    )

    class Meta:
        ordering = ('-user',)
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                name='unique_follow',
                fields=['user', 'author']
            ),
            models.CheckConstraint(
                name='follow is not follower',
                check=~models.Q(user=models.F('author'))
            )]

    def __str__(self):
        return self.author.username
