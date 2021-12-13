import tempfile
from django.urls import reverse
from django.test import Client, TestCase

from ..models import Post, Group, User, Comment
from.test_views import CRATE_URL


class PostFormTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.image = tempfile.NamedTemporaryFile(suffix=".jpg").name
        cls.user = User.objects.create_user(username='test_2')
        cls.group = Group.objects.create(
            title='Заголовок PostFormTest',
            description='Текст',
            slug='test-slug_3',
        )

        cls.post = Post.objects.create(
            text='Заголовок PostFormTest',
            group=cls.group,
            author=cls.user,
        )

        cls.comment = Comment.objects.create(
            text='комментарий',
            post=cls.post,
            author=cls.user,
        )

        cls.post_edit_url = reverse('posts:post_edit', args=(cls.post.id,))
        cls.profile_url = reverse('posts:profile', args=(cls.user,))
        cls.post_detail_url = reverse('posts:post_detail', args=(cls.post.id,))
        cls.add_comment_url = reverse('posts:add_comment', args=(cls.post.id,))

    def setUp(self):
        self.not_authorized_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_post(self):
        """Валидная форма создает запись в Post."""
        user = self.__class__.user
        post_count = Post.objects.count()
        form_data = {
            'text': 'Тестовый текст post_create',
            'group': self.__class__.group.id,
            'author': user,
            'image': self.__class__.image
        }
        response = self.authorized_client.post(
            CRATE_URL,
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, self.profile_url)
        self.assertEqual(Post.objects.count(), post_count + 1)
        self.assertTrue(
            Post.objects.filter(
                text=form_data['text'],
                group=form_data['group']
            ).exists()
        )

    def test_post_edit(self):
        """Валидная форма Изменяет Post."""
        post = self.__class__.post
        post_count = Post.objects.count()
        form_data = {
            'text': 'Тестовый текст post_create_фывфыв',
            'group': self.__class__.group.id,
            'author': self.__class__.user.id
        }
        response = self.authorized_client.post(
            self.post_edit_url,
            data=form_data,
            follow=True
        )
        self.assertEqual(Post.objects.count(), post_count)
        self.assertNotEqual(response.context['post'].text, post.text)
        self.assertRedirects(response, self.post_detail_url)

    def test_comment_authorized(self):
        """Валидная форма Добавляет коммент"""
        form_data = {
            'text': self.comment.text
        }
        response = self.authorized_client.post(
            self.add_comment_url,
            data=form_data,
            follow=True
        )

        self.assertTrue(
            Comment.objects.filter(
                text=form_data['text']
            ).exists())
        self.assertRedirects(response, self.post_detail_url)

    def test_comment_not_authorized(self):
        """Не вошедший пользователь не может комментировать посты."""
        form_data = {
            'text': 'sdfsdfdsfds'
        }
        response = self.not_authorized_client.post(
            self.add_comment_url,
            data=form_data,
            follow=True
        )

        self.assertFalse(
            Comment.objects.filter(
                text=form_data['text']
            ).exists())

    def test_initial_value(self):
        """Предустановленнное значение формы post_edit."""
        response = self.authorized_client.get(self.post_edit_url)
        text_inital = response.context['form']['text'].initial
        group_inital = response.context['form']['group'].initial
        self.assertEqual(text_inital, self.__class__.post.text)
        self.assertEqual(group_inital, self.__class__.post.group.id)
