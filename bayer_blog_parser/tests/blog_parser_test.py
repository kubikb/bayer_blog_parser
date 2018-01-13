import codecs
import os
import requests_mock
import unittest

from bayer_blog_parser.blog_parser import BayerBlogParser, BayerBlogParserException

DATA_FOLDER = os.path.join(os.path.dirname(__file__), u'data')
test_page_content = codecs.open(os.path.join(DATA_FOLDER, "page_full_html.html"), "r", "utf-8").read()
empty_page_content = codecs.open(os.path.join(DATA_FOLDER, "empty_page.html"), "r", "utf-8").read()
base_url = "https://badog.blogstar.hu"

class TestBlogParser(unittest.TestCase):

	def test_init_wrong_depth(self):
		with self.assertRaises(BayerBlogParserException):
			BayerBlogParser(depth="wrong_input")

	def test_depth_larger_than_total_num_pages(self):
		with requests_mock.mock() as m:
			m.get(base_url, text=test_page_content)

			parser = BayerBlogParser(depth=999999)
			self.assertEqual(parser.depth, 114)

	def test_collect_posts(self):
		depth = 12

		with requests_mock.mock() as m:

			# Main page
			m.get(base_url, text=test_page_content)

			for i in range(1, depth):
				m.get('%s/?p=%s' % (base_url, i),
					  text=test_page_content)

			parser = BayerBlogParser(depth=depth)
			blogposts = parser.list_all_posts()
			self.assertEqual(len(blogposts), 10 * (depth))

	def test_get_last_page_index(self):
		with requests_mock.mock() as m:
			m.get(base_url, text=test_page_content)

			parser = BayerBlogParser()
			last_page_index = parser.get_last_page_index()

			self.assertEqual(last_page_index, 114)
