from django.test import TestCase
from catalog.models import Author


class AuthorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Author.objects.create(first_name='Big', last_name='Bob')

    def test_first_name_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, 'First Name:')

    def test_first_name_max_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('first_name').max_length
        self.assertEqual(max_length, 100)



## dobavit 2 class, in each 3 methods in here for all models


# class YourTestClass(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         print('Clean data was created here')
#         pass
#
#     def setUp(self) -> None:
#         print('Zapust tolka odin raz')
#         pass
#
#     def test_false_is_false(self):
#         print('Test stupid things')
#         self.assertFalse(False)
#
#     def test_false_is_true(self):
#         print('Test 2 stupid things')
#         self.assertTrue(False)
#
#     def test_one_plus_one_equal(self):
#         print('1+1=2')
#         self.assertEqual(1 + 1, 2)
