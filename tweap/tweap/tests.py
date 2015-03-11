from django.test import TestCase
from tweap.tools import StringParser


class ToolsTest(TestCase):

    def test_string_parser(self):
        sp = StringParser({'@': 'users', '#': 'tags'}, 'title')
        data = sp.parse('Hallo @thomas @tobi #yolo #swag')
        self.assertEqual(data, {'title': 'Hallo', 'tags': ['yolo', 'swag'], 'users': ['thomas', 'tobi']})

        data = sp.parse('Hallo')
        self.assertEqual(data, {'title': 'Hallo', 'tags': [], 'users': []})

        sp2 = StringParser({'@': 'at', '#': 'hashtags'}, 'title')
        data2 = sp2.parse('Hallo @thomas #tobi @lo #swag')
        self.assertEqual(data2, {'title': 'Hallo', 'hashtags': ['tobi', 'swag'], 'at': ['thomas', 'lo']})

        data2 = sp2.parse('Hallo')
        self.assertEqual(data2, {'title': 'Hallo', 'hashtags': [], 'at': []})

