from http import HTTPStatus
from django.test import Client, TestCase
from django.urls import reverse


#  URLS
AUTHOR_URL = reverse('about:author')
TECH_URL = reverse('about:tech')

#  TEMPLATES
AUTHOR_TEMP = 'about/author.html'
TECH_TEMP = 'about/tech.html'


class AboutTests(TestCase):
    def setUp(self):
        self.not_authorized_client = Client()

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            AUTHOR_URL: AUTHOR_TEMP,
            TECH_URL: TECH_TEMP
        }

        for url, template in templates_url_names.items():
            with self.subTest(url=url):
                response = self.not_authorized_client.get(url)
                self.assertTemplateUsed(response, template)

    def test_url_for_not_authorized_client(self):
        """URL-адреса доступны  НЕ аутентифицированному пользователю."""
        url = (AUTHOR_URL, TECH_URL)
        for url in url:
            with self.subTest(url=url):
                response = self.not_authorized_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)
