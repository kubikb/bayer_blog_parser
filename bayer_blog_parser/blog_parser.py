from joblib import Parallel, delayed
import logging as log
import requests

# Custom exception
from bayer_blog_parser.blog_page import BlogPage


class BayerBlogParserException(Exception):
	pass

# Outside of class so that joblib can pickle it..
def process_one_post(blog_post):
	return {
		"url": blog_post.url,
		"title": blog_post.title,
		"author": blog_post.author,
		"lead_text": blog_post.lead_text,
		"thumbnail_url": blog_post.thumbnail_url,
		"date": blog_post.date,
		"full_content": blog_post.full_content
	}


class BayerBlogParser:

	depth = None

	__blogposts = None
	__BASE_URL = "https://badog.blogstar.hu"
	__POSTS_PER_PAGE = 10

	def __init__(self, depth=None):
		log.debug("Initializing BayerBlogParser instance...")
		if depth is not None:
			if not isinstance(depth, int):
				raise BayerBlogParserException("Please provide an integer as depth!")

			self.depth = depth
			log.info("Depth is set to %s." % depth)

		log.debug("Successfully initialized BayerBlogParser instance!")

	def list_all_posts(self):
		if self.__blogposts is not None:
			return self.__blogposts

		log.info("Parsing blog pages to collect posts in progress...")

		all_blogposts = []

		i = 1	# Counter
		is_done = False
		while not is_done:
			blogposts = self.__process_one_page(i)
			if len(blogposts) > 0:
				all_blogposts += blogposts

			if len(blogposts) < self.__POSTS_PER_PAGE:
				is_done = True

			if i == self.depth:
				is_done = True

			i += 1

		log.info("Successfully collected all blog posts! There are %s posts in total." % len(all_blogposts))
		self.__blogposts = all_blogposts
		return all_blogposts

	def parse_all_posts(self, n_jobs=-1):
		blogposts = self.__blogposts
		if blogposts is None:
			blogposts = self.list_all_posts()

		return Parallel(n_jobs=n_jobs)(delayed(process_one_post)(post) for post in blogposts) #[self.__process_one_post(post) for post in blogposts]

	def __process_one_page(self, page_index):

		content = self.__get_page_content(
			"%s/?p=%s" % (self.__BASE_URL, page_index)
		)
		page = BlogPage(page_index=page_index, content=content)
		blogposts = page.blogposts
		return blogposts

	def __get_page_content(self, url):
		log.info("Opening %s is in progress..." % url)
		return requests.get(url).text
