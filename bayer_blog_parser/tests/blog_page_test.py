import codecs
import os
import unittest

from bayer_blog_parser.blog_page import BlogPage
from bayer_blog_parser.blog_post import BlogPost

DATA_FOLDER = os.path.join(os.path.dirname(__file__), u'data')
test_page_content = codecs.open(os.path.join(DATA_FOLDER, "page_full_html.html"), "r", "utf-8").read()
empty_page_content = codecs.open(os.path.join(DATA_FOLDER, "empty_page.html"), "r", "utf-8").read()

class TestBlogPage(unittest.TestCase):

	def test_blogposts(self):
		page = BlogPage(page_index=15, content=test_page_content)
		blogposts = page.blogposts
		for post in blogposts:
			self.assertIsInstance(post, BlogPost)

		self.assertEqual(len(blogposts), 10)

	def test_empty_page(self):
		page = BlogPage(page_index=99, content=empty_page_content)
		blogposts = page.blogposts
		self.assertEqual(len(blogposts), 0)