import tempfile
from django import forms
from django.test import Client, TestCase
from django.urls import reverse
from django.conf import settings as conf_settings

from ..models import Post, Group, User, Comment

TITLE_DICT = conf_settings.TITLE_DICT
PAGE_COUNT = conf_settings.PAGINATOR_COUNT_PAGE

HOME_URL = reverse('posts:index')
CRATE_URL = reverse('posts:post_create')
FOLLOW_URL = reverse('posts:follow_index')


class PostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.image = tempfile.NamedTemporaryFile(suffix=".jpg").name
        cls.user = User.objects.create_user(username='test')
        cls.group = Group.objects.create(
            title='Заголовок',
            description='Текст',
            slug='test-slug',
        )
        cls.post = Post.objects.create(
            text='Заголовок',
            group=cls.group,
            author=cls.user,
            image=cls.image
        )

        cls.comment = Comment.objects.create(
            text='комментарий',
            post=cls.post,
            author=cls.user,
        )

        cls.post_edit_url = reverse('posts:post_edit', args=(cls.post.id,))
        cls.profile_url = reverse('posts:profile', args=(cls.user,))
        cls.post_detail_url = reverse('posts:post_detail', args=(cls.post.id,))
        cls.group_lst_url = reverse('posts:group_list', args=(cls.group.slug,))

    def setUp(self):
        self.user = self.__class__.user
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_post_detail_page_show_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        response = self.authorized_client.get(self.post_detail_url)
        comment = response.context['comments'][0]
        first_object = response.context['post']
        self.assertEqual(first_object.id, self.__class__.post.id)
        self.assertEqual(first_object.image, self.__class__.image)
        self.assertEqual(first_object.image, self.__class__.image)
        self.assertEqual(comment, self.__class__.comment)

    def test_group_detail_page_show_correct_context(self):
        """Шаблон group_list сформирован с правильным контекстом."""
        response = self.authorized_client.get(self.group_lst_url)
        first_object = response.context['group']
        post = response.context['page_obj'][0]
        self.assertEqual(first_object.id, self.__class__.group.id)
        self.assertEqual(post.image, self.__class__.image)

    def test_homepage_page_show_correct_context(self):
        """Шаблон homepage сформирован с правильным контекстом."""
        response = self.authorized_client.get(HOME_URL)
        post = response.context['page_obj'][0]
        self.assertEqual(post.image, self.__class__.image)

    def test_post_create_page_show_correct_context(self):
        """Шаблон post_create сформирован с правильным контекстом."""
        response = self.authorized_client.get(CRATE_URL)
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }

        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_post_edit_page_show_correct_context(self):
        """Шаблон post_edit сформирован с правильным контекстом."""
        response = self.authorized_client.get(self.post_edit_url)
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }

        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test__paginator(self):
        """Пгинатор ввыводин заданнове кол - во обьектов"""
        for post in range(13):
            Post.objects.create(
                text=f'Заголовок{post}',
                author=self.user,
                group=self.__class__.group)

        urls = (HOME_URL,
                self.group_lst_url,
                self.profile_url
                )

        for url in urls:
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertEqual(len(response.context['page_obj']), PAGE_COUNT)
