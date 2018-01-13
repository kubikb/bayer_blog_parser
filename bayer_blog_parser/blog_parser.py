from joblib import Parallel, delayed
import logging as log
import urlparse
from bayer_blog_parser.blog_page import BlogPage
import bayer_blog_parser.connection_utils as conn_utils

# Custom exception
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

def process_one_page(page_url, page_index):
	content = conn_utils.open_url(page_url)
	page = BlogPage(page_index=page_index, content=content)
	return page.blogposts

class BayerBlogParser:

	__depth = None
	__blogposts = None
	__total_pages_count = None

	__BASE_URL = "https://badog.blogstar.hu"
	__POSTS_PER_PAGE = 10

	@property
	def depth(self):
		return self.__depth

	def __init__(self, depth=None):
		log.debug("Initializing BayerBlogParser instance...")

		total_pages_count = int(self.get_last_page_index())
		self.__total_pages_count = total_pages_count

		if depth is not None:
			if not isinstance(depth, int):
				raise BayerBlogParserException("Please provide an integer as depth!")

			if depth > total_pages_count:
				log.warn("Depth (%s) is set to a larger number as the total number of pages! Setting depth to the total number of pages (%s) in the blog." %(depth, total_pages_count))
				depth = total_pages_count

		else:
			depth = total_pages_count

		self.__depth = depth
		log.info("Depth is set to %s." % depth)

		log.debug("Successfully initialized BayerBlogParser instance!")

	def list_all_posts(self, n_jobs=-1):
		if self.__blogposts is not None:
			return self.__blogposts

		log.info("Parsing blog pages to collect posts in progress...")

		range_page_indices = range(1, self.__depth + 1)
		all_pages = Parallel(n_jobs=n_jobs)\
			(delayed(process_one_page)(
				self.__get_page_url(i), i
			) for i in range_page_indices)

		all_blogposts = [item for sublist in all_pages for item in sublist]

		log.info("Successfully collected all blog posts! There are %s posts in total." % len(all_blogposts))
		self.__blogposts = all_blogposts
		return all_blogposts

	def parse_all_posts(self, n_jobs=-1):
		blogposts = self.__blogposts
		if blogposts is None:
			blogposts = self.list_all_posts()

		return Parallel(n_jobs=n_jobs)(delayed(process_one_post)(post) for post in blogposts)

	def get_last_page_index(self):
		log.debug("Obtaining the index of last page in progress...")
		content = conn_utils.get_soup_from_url(self.__BASE_URL)
		right_pager = content.find("div", {"class": "rightPager"})
		last_url_in_pager = right_pager.findAll("a")[-1].get("href")

		# Parse url
		parsed_url = urlparse.urlparse(last_url_in_pager)
		url_query_params = urlparse.parse_qs(parsed_url.query)
		page_num_query_param = url_query_params.get("p")

		if page_num_query_param is None:
			raise BayerBlogParserException("Could not find the index of the last page!")

		last_page_index = int(page_num_query_param[0])
		log.debug("The last page of the blog is number %s!" % last_page_index)
		return last_page_index

	def __process_one_page(self, page_index):
		content = conn_utils.open_url(
			"%s/?p=%s" % (self.__BASE_URL, page_index)
		)
		page = BlogPage(page_index=page_index, content=content)
		blogposts = page.blogposts
		return blogposts

	def __get_page_url(self, page_index):
		return "%s/?p=%s" % (self.__BASE_URL, page_index)
