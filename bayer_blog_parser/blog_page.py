import logging as log

from bayer_blog_parser.blog_post import BlogPost
import connection_utils as conn_utils


class BlogPage:
	__blogposts = None
	__content_soup = None

	def __init__(self, page_index, content):
		log.debug("Initializing BlogPage instance...")

		self.page_index = page_index
		log.debug("Page index is set to %s." % page_index)

		log.debug("Attempting to parse page content at page %s." % page_index)
		self.__content_soup = conn_utils.get_soup_from_page_content(content)

		log.debug("Initializing BlogPage was successful!")

	@property
	def page_index(self):
		return self.page_index

	@page_index.setter
	def page_index(self, page_index):
		self.page_index = page_index

	@property
	def blogposts(self):
		if self.__blogposts is not None:
			return self.__blogposts

		log.debug("Obtaining posts from page %s." % self.page_index)
		soup = self.__content_soup

		blogpost_components = soup.findAll("section", {"class": "blogPost"})
		log.debug("Found %s posts on page %s!"
				  % (len(blogpost_components), self.page_index))

		blogposts = [BlogPost(content) for content in blogpost_components]

		self.__blogposts = blogposts

		return blogposts