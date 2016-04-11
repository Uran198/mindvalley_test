from unittest import TestCase

from cv import data_to_html, escape_data, urlize_data


class DataToHtmlTests(TestCase):

    def test_raw_data(self):
        data = "Some text"
        expected = "<p>Some text</p>"
        self.assertEqual(data_to_html(data), expected)

    def test_dict_with_raw_data(self):
        data = {"key0": "value0", "key1": "value1"}
        # dict has no order
        expected = ['<div><p class="key0">value0</p>'
                    '<p class="key1">value1</p></div>',
                    '<div><p class="key1">value1</p>'
                    '<p class="key0">value0</p></div>']
        self.assertIn(data_to_html(data), expected)

    def test_dict_with_list(self):
        data = {"key0": ["value0", "value1"]}
        expected = ('<div><ul class="key0"><li><p>value0</p></li>'
                    '<li><p>value1</p></li></ul></div>')
        self.assertEqual(data_to_html(data), expected)

    def test_dict_with_dict(self):
        data = {"key0": {"inner": "value"}}
        expected = ('<div><div class="key0">'
                    '<p class="inner">value</p></div></div>')
        self.assertEqual(data_to_html(data), expected)

    def test_list_with_raw_data(self):
        data = ["asd", "asd1"]
        expected = '<ul><li><p>asd</p></li><li><p>asd1</p></li></ul>'
        self.assertEqual(data_to_html(data), expected)

    def test_list_with_dict(self):
        data = [{"key0": "value0"}, {"key1": "value1"}]
        expected = ('<ul><li><div><p class="key0">value0</p></div></li>'
                    '<li><div><p class="key1">value1</p></div></li></ul>')
        self.assertEqual(data_to_html(data), expected)

    def test_list_with_list(self):
        data = ["value0", ["value1", "value2"]]
        expected = ('<ul><li><p>value0</p></li><li><ul><li><p>value1</p></li>'
                    '<li><p>value2</p></li></ul></li></ul>')
        self.assertEqual(data_to_html(data), expected)

    def test_nested_dict(self):
        data = {"key0": {"key1": [{"key2": "value2"}]}}
        expected = ('<div><div class="key0"><ul class="key1"><li><div>'
                    '<p class="key2">value2</p></div></li></ul></div></div>')
        self.assertEqual(data_to_html(data), expected)


class EscapeDataTest(TestCase):

    def test_raw_string(self):
        data = '<scr"'
        expected = '&lt;scr&quot;'
        self.assertEqual(escape_data(data), expected)

    def test_list(self):
        data = ['<scr"']
        expected = ['&lt;scr&quot;']
        self.assertEqual(escape_data(data), expected)

    def test_dict(self):
        data = {'cls"': '<scr"'}
        expected = {'cls&quot;': '&lt;scr&quot;'}
        self.assertEqual(escape_data(data), expected)

    def test_dict_with_list(self):
        data = {'cls"': ['<scr"']}
        expected = {'cls&quot;': ['&lt;scr&quot;']}
        self.assertEqual(escape_data(data), expected)

    def test_list_with_dict(self):
        data = [{'cls"': '<scr"'}]
        expected = [{'cls&quot;': '&lt;scr&quot;'}]
        self.assertEqual(escape_data(data), expected)

    def test_deep_nested_dict(self):
        data = {'cls"': {'"': [{'>': '<scr"'}]}}
        expected = {'cls&quot;': {'&quot;': [{'&gt;': '&lt;scr&quot;'}]}}
        self.assertEqual(escape_data(data), expected)


class UrlizeDataTest(TestCase):

    def test_raw(self):
        data = 'github https://github.com/'
        expected = ('github <a href="https://github.com/">'
                    'https://github.com/</a>')
        self.assertEqual(urlize_data(data), expected)

    def test_list(self):
        data = ['github https://github.com/']
        expected = [('github <a href="https://github.com/">'
                    'https://github.com/</a>')]
        self.assertEqual(urlize_data(data), expected)

    def test_dict(self):
        data = {'github': 'https://github.com/'}
        expected = {'github': ('<a href="https://github.com/">'
                               'https://github.com/</a>')}
        self.assertEqual(urlize_data(data), expected)
