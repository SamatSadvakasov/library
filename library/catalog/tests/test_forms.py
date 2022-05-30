import datetime

from django.test import TestCase
from django.utils import timezone

from catalog.forms import RenewBookForm


class RenewBookFormTest(TestCase):
    def test_renew_form_date_field_label(self):
        form = RenewBookForm()

        self.assertTrue(form.fields['renewal_date'].label is None or
                        form.fields['renewal_date'].label == 'renewal date')

    def test_renew_form_date_in_past(self):
        date = datetime.date.today() - datetime.timedelta(days=1)
        form = RenewBookForm(data={'renewal_date': date})
        self.assertFalse(form.is_valid())

    # Check if a date is in the allowed range (+4 weeks from today).
    # add additional 3 methods
