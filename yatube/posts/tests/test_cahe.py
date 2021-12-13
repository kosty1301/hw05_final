import tempfile

from django.test import Client, TestCase
from django.conf import settings as conf_settings

from .test_views import HOME_URL
from ..models import Post, User


TITLE_DICT = conf_settings.TITLE_DICT
PAGE_COUNT = conf_settings.PAGINATOR_COUNT_PAGE


class Testcache(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.image = tempfile.NamedTemporaryFile(suffix=".jpg").name
        cls.user = User.objects.create_user(username='test')
        cls.post = Post.objects.create(
            text='Заголовок',
            author=cls.user,
            image=cls.image
        )

    def setUp(self):
        self.user = self.__class__.user
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_homepage_page_show_correct_context(self):
        """ Тестирование кэша"""
        Post.objects.create(
            text='Заголовок sdfds',
            author=self.__class__.user,
            image=self.__class__.image
        )

        response = self.authorized_client.get(HOME_URL)
        post = response.context['page_obj'][0]
        self.assertEqual(post.text, post.text)

        post.delete()

        response = self.authorized_client.get(HOME_URL)
        post = response.context['page_obj'][0]
        self.assertEqual(post.text, post.text)
