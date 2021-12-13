from django.test import TestCase

from ..models import Post, Group, User


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа PostModelTest',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовая группа PostModelTest',
        )
        cls.obj = {cls.post.text[:15]: PostModelTest.post,
                   cls.group.title: PostModelTest.group}

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        for result, obj in self.obj.items():
            self.assertEqual(obj.__str__(), result)
