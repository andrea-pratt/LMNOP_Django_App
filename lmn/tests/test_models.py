import tempfile
import filecmp
import os

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User 
from django.db import IntegrityError

from ..models import Show

# Create your tests here.


class TestUser(TestCase):

    def test_create_user_duplicate_username_fails(self):

        user = User(username='bob', email='bob@bob.com', first_name='bob', last_name='bob')
        user.save()

        user2 = User(username='bob', email='another_bob@bob.com', first_name='bob', last_name='bob')
        with self.assertRaises(IntegrityError):
            user2.save()


    def test_create_user_duplicate_email_fails(self):
        user = User(username='bob', email='bob@bob.com', first_name='bob', last_name='bob')
        user.save()

        user2 = User(username='bob', email='bob@bob.com', first_name='bob', last_name='bob')
        with self.assertRaises(IntegrityError):
            user2.save()


class TestShow(TestCase):

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.client.force_login(self.user)
        
    def test_create_new_show(self):
        fixtures = ['testing_artists', 'testing_venues']

        response = self.client.post(reverse('add_show'), { 'show_date': '12/21/21', 'show_time': '19:00:00', 'artist': 'REM',  'venue': 'First Avenue'}, follow=True)

        self.assertTemplateUsed(response, 'lmn/show_add.html')

        response_shows = response.context['shows']

        show_in_database = Show.objects.get(showdate='12/21/21', show_time='19:00:00')

        self.assertEqual(response_shows, show_in_database)