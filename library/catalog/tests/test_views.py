from django.test import TestCase
from django.urls import reverse
from catalog.models import Author
from django.contrib.auth.models import User


class AuthorListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_authors = 13
        for author_id in range(number_of_authors):
            Author.objects.create(
                first_name=f'Christian {author_id}',
                last_name=f'Surname {author_id}'
            )

    def setUp(self) -> None:
        test_user1 = User.objects.create_user(username='testuser1', password='QAZqaz123')
        test_user1.save()

    def test_view_url_accessible_by_name(self):
        self.client.login(username='testuser1', password='QAZqaz123')
        response = self.client.get('/catalog/authors/')  # /catalog/authors/
        self.assertEqual(response.status_code, 200)

    def test_pagination_is_ten(self):
        self.client.login(username='testuser1', password='QAZqaz123')
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['author_list']), 10)

# 3 CLASS each 3 methods
