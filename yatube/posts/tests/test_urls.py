from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse

from ..models import Post, Group, User

#  STATIC_URLS
HOME_URL = '/'
CREATE_URL = '/create/'
FOLLOW_URL = '/follow/'

#  TEMPLATES
INDEX = 'posts/index.html'
CREATE = 'posts/post_create.html'
DETAIL = 'posts/post_detail.html'
PROFILE = 'posts/profile.html'
GROUP_LIST = 'posts/group_list.html'
FOLLOW = 'posts/follow.html'


class PostUrlsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='testurl')
        cls.group = Group.objects.create(
            title='Заголовок',
            description='Текст',
            slug='test-slug',
        )
        cls.post = Post.objects.create(
            text='Заголовок',
            group=cls.group,
            author=cls.user
        )

        cls.post_edit_url = f'/posts/{cls.post.id}/edit/'
        cls.post_detail_url = f'/posts/{cls.post.id}/'
        cls.profile_url = f'/profile/{cls.user}/'
        cls.group_post_url = f'/group/{cls.group.slug}/'
        cls.add_comment_url = f'posts/{cls.post.id}/comment'

    def setUp(self):
        self.not_authorized_client = Client()
        self.user = PostUrlsTests.user
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            HOME_URL: INDEX,
            CREATE_URL: CREATE,
            FOLLOW_URL: FOLLOW,
            self.post_edit_url: CREATE,
            self.post_detail_url: DETAIL,
            self.profile_url: PROFILE,
            self.group_post_url: GROUP_LIST
        }
        for url, template in templates_url_names.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template)

    def test_url_for_authorized_client(self):
        """URL-адреса доступны аутентифицированному пользователю."""
        exists_for_authorized_client = (
            HOME_URL,
            CREATE_URL,
            self.post_edit_url,
            self.post_detail_url,
            self.profile_url,
            self.group_post_url,
        )

        for url in exists_for_authorized_client:
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_url_for_not_authorized_client(self):
        """URL-адреса НЕ доступны  не вошедшему пользователю."""
        url = (self.post_edit_url, CREATE_URL, FOLLOW_URL)
        for url in url:
            with self.subTest(url=url):
                response = self.not_authorized_client.get(url)
                self.assertRedirects(response, f'/auth/login/?next={url}')

    def test_post_edit_for_not_author(self):
        """Страница редакт. поста доступна только автору"""
        user = User.objects.create_user(username='testauthor')
        post = Post.objects.create(
            text='Заголовок',
            author=user
        )
        url = f'/posts/{post.id}/edit/'
        response = self.authorized_client.get(url)
        destination = reverse('posts:post_detail', kwargs={'post_id': post.id})
        self.assertRedirects(response, destination)
        url = self.post_edit_url
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
