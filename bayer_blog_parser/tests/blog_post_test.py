# coding=utf-8
from bs4 import BeautifulSoup
import codecs
import os
import requests_mock
import unittest

from bayer_blog_parser.blog_post import BlogPost

DATA_FOLDER = os.path.join(os.path.dirname(__file__), u'data')
test_post_soup = BeautifulSoup(
	file(os.path.join(DATA_FOLDER, "post.html"), "r").read(),
	"html.parser"
)
test_post_content = codecs.open(os.path.join(DATA_FOLDER, "post_full_html.html"), "r", "utf-8").read()

test_post_text = codecs.open(os.path.join(DATA_FOLDER, "post_content.txt"), "r", "utf-8").read()

class TestBlogPost(unittest.TestCase):

	def test_date(self):
		test_instance = BlogPost(test_post_soup)
		self.assertEqual(test_instance.date, "2017.12.29.")

	def test_thumbnail_url(self):
		test_instance = BlogPost(test_post_soup)
		self.assertEqual(
			test_instance.thumbnail_url,
			"./pages/badog/contents/blog/46467/pics/lead_800x600.jpg"
		)

	def test_missing_thumbnail(self):
		post_soup = BeautifulSoup(
			file(os.path.join(DATA_FOLDER, "post_without_thumbnail.html"), "r").read(),
			"lxml"
		)
		test_instance = BlogPost(post_soup)
		self.assertEqual(
			test_instance.thumbnail_url,
			None
		)

	def test_url(self):
		test_instance = BlogPost(test_post_soup)
		self.assertEqual(
			test_instance.url,
			"https://badog.blogstar.hu/2017/12/29/vendegszerzo-muve/46467/"
		)

	def test_title(self):
		test_instance = BlogPost(test_post_soup)
		self.assertEqual(
			test_instance.title,
			u"Vendégszerző műve"
		)

	def test_author(self):
		test_instance = BlogPost(test_post_soup)
		self.assertEqual(
			test_instance.author,
			u"Bayer Zsolt"
		)

	def test_lead_text(self):
		test_instance = BlogPost(test_post_soup)
		self.assertEqual(
			test_instance.lead_text,
			u"Tóth Tamara írta az alábbi cikket, Bécsből kaptam, fogadják szeretettel."
		)

	def test_full_content(self):
		test_instance = BlogPost(test_post_soup)

		# Mocking requests
		with requests_mock.mock() as m:
			m.get('https://badog.blogstar.hu/2017/12/29/vendegszerzo-muve/46467/',
				  text=test_post_content)

			full_content = test_instance.full_content
			self.assertEqual(full_content, test_post_text)