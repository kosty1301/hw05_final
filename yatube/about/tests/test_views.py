from http import HTTPStatus

from django.test import Client, TestCase

from test_urls import AUTHOR_URL, TECH_URL
from django.conf import settings as conf_settings


TITLE_DICT = conf_settings.TITLE_DICT


class AboutTests(TestCase):
    def setUp(self):
        self.not_authorized_client = Client()
        self.author_url = AUTHOR_URL
        self.tach_url = TECH_URL
        self.title_Author = TITLE_DICT.get('AboutAuthor')
        self.tech_title = TITLE_DICT.get('TechAuthor')

    def test_url_for_not_authorized_client(self):
        """Шаблон  сформирован с правильным контекстом."""
        urls_and_title = {
            AUTHOR_URL: self.title_Author,
            TECH_URL: self.tech_title
        }
        for url, title in urls_and_title.items():
            with self.subTest(url=url):
                response = self.not_authorized_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)
                self.assertEqual(response.context['title'], title)
