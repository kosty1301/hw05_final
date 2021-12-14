import tempfile

from django.test import TestCase

from ..models import Post, Group, User, Comment, Follow


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.user_follower = User.objects.create_user(username='follower')
        cls.group = Group.objects.create(
            title='Тестовая группа PostModelTest',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовая группа PostModelTest',
        )
        cls.comment = Comment.objects.create(
            text='комментарий',
            post=cls.post,
            author=cls.user,
        )
        cls.follow = Follow.objects.create(
            user=cls.user_follower,
            author=cls.user
        )

        cls.obj = {cls.post.text[:15]: cls.post,
                   cls.group.title: cls.group,
                   cls.follow.author.username: cls.user.username
                   }

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        for result, obj in self.obj.items():
            self.assertEqual(obj.__str__(), result)
