import codecs
import os
import requests_mock
import unittest

from bayer_blog_parser.blog_parser import BayerBlogParser, BayerBlogParserException

DATA_FOLDER = os.path.join(os.path.dirname(__file__), u'data')
test_page_content = codecs.open(os.path.join(DATA_FOLDER, "page_full_html.html"), "r", "utf-8").read()
empty_page_content = codecs.open(os.path.join(DATA_FOLDER, "empty_page.html"), "r", "utf-8").read()
base_url = "https://badog.blogstar.hu"

class TestBayerBlogParser(unittest.TestCase):

	def test_init_wrong_depth(self):
		with self.assertRaises(BayerBlogParserException):
			BayerBlogParser(depth="wrong_input")

	def test_collect_posts(self):
		num_pages = 13
		depth = 999

		with requests_mock.mock() as m:
			for i in range(1, num_pages):
				m.get('%s/?p=%s' % (base_url, i),
					  text=test_page_content)

			# Last page
			m.get('%s/?p=%s' % (base_url, num_pages),
				  text=empty_page_content)

			parser = BayerBlogParser(depth=depth)
			blogposts = parser.list_all_posts()
			self.assertEqual(len(blogposts), 10 * (num_pages - 1))
