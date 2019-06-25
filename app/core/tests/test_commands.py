from unittest.mock import patch

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


class CommandsTestCase(TestCase):

    def test_wait_for_db_ready(self):
        """Wait for db when db is already available."""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.return_value = True
            call_command('wait_for_db')

            self.assertEqual(1, gi.call_count)

    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, time_sleep):
        """Wait for db to be available."""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')

            self.assertEqual(6, gi.call_count)
