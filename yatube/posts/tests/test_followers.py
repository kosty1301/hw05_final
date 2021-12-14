from django.urls import reverse
from django.test import Client, TestCase
from django.db import IntegrityError

from ..models import Post, User, Follow
from.test_views import FOLLOW_URL


class PostFormTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='FormTest')
        cls.post = Post.objects.create(
            text='Заголовок PostFormTest',
            author=cls.user,
        )

        cls.profile_follow_url = reverse(
            'posts:profile_follow',
            args=(cls.user,)
        )
        cls.profile_unfollow_url = reverse(
            'posts:profile_unfollow',
            args=(cls.user,)
        )
        cls.profile_url = reverse('posts:profile', args=(cls.user,))

    def setUp(self):
        self.not_authorized_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_follow_not_auth(self):
        """Не впшедший  пользователь не может подписываться на других."""
        response = self.not_authorized_client.get(self.profile_follow_url)
        self.assertRedirects(
            response,
            f'/auth/login/?next={self.profile_follow_url}'
        )

    def test_follow_auth(self):
        """Пользователь может подписываться и отписываться на других."""
        follower = User.objects.create_user(username='follower')
        follower_client = Client()
        follower_client.force_login(follower)
        resp_to_follow = follower_client.get(self.profile_follow_url)
        self.assertTrue(Follow.objects.filter(
            user=follower, author=self.user).exists())
        self.assertRedirects(resp_to_follow, self.profile_url)

        #  unfollow
        follower_client.get(self.profile_unfollow_url)
        self.assertFalse(Follow.objects.filter(
            user=follower, author=self.user).exists())

    def test_followers_posts(self):
        """Новая запись пользователя появляется в ленте тех,
        кто на него подписан и не появляется в ленте тех, кто не подписан."""

        follower = User.objects.create_user(username='test_followers')
        follower_client = Client()
        follower_client.force_login(follower)
        resp_to_follow = follower_client.get(self.profile_follow_url)
        self.assertTrue(Follow.objects.filter(
            user=follower, author=self.user).exists())
        self.assertRedirects(resp_to_follow, self.profile_url)

        response = follower_client.get(FOLLOW_URL)
        post = response.context['page_obj'][0]
        self.assertEqual(post.author, self.__class__.user)

        # not follow
        not_follower = User.objects.create_user(username='not_follower')
        follower_client = Client()
        follower_client.force_login(not_follower)
        response = follower_client.get(FOLLOW_URL)
        context = response.context['page_obj']
        if len(context) != 0:
            self.assertNotEqual(context[0].author, self.__class__.user)

    def test_no_self_follow(self):
        user = User.objects.create(username='self')
        """USER не может подписатся на самого себя."""
        constraint_name = 'follow is not follower'
        with self.assertRaisesMessage(IntegrityError, constraint_name):
            Follow.objects.create(author=user, user=user)

    def test_follow(self):
        """USER может подписатся только один раз."""
        author = User.objects.create(username='gfhfgh')
        user = User.objects.create(username='ghfg')
        Follow.objects.create(author=author, user=user)
        with self.assertRaises(IntegrityError) as context:
            Follow.objects.create(author=author, user=user)
        self.assertTrue('UNIQUE constraint failed' in str(context.exception))
