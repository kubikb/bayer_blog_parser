import logging as log
import bayer_blog_parser.connection_utils as conn_utils


class BlogPost:

	__full_content = None
	__content_soup = None

	def __init__(self, content_soup):
		log.debug("Initializing BlogPost instance...")

		self.__content_soup = content_soup
		log.debug("Page content set successfully.")

		log.debug("Initializing BlogPost was successful!")

	@property
	def url(self):
		soup = self.__content_soup
		title_component = self.__parse_title_component(soup)
		a_tag = title_component.find("a")
		return a_tag["href"]

	@property
	def title(self):
		soup = self.__content_soup
		title_component = self.__parse_title_component(soup)
		a_tag = title_component.find("a")
		return a_tag.getText()

	@property
	def author(self):
		soup = self.__content_soup
		inforow = soup.find("div", {"class": "inforow"})
		author_name = inforow.find("div", {"class": "authorname"})
		return author_name.getText()

	@property
	def lead_text(self):
		soup = self.__content_soup
		lead_text_item = soup.find("div", {"class": "lead"})
		return lead_text_item.getText()

	@property
	def thumbnail_url(self):
		soup = self.__content_soup
		pic_content = self.__parse_pic_content(soup)
		pic_div = pic_content\
			.find("div", {"class": "pic"})

		if pic_div is None:
			return None

		return pic_div.find("img")["src"]

	@property
	def date(self):
		soup = self.__content_soup
		pic_content = self.__parse_pic_content(soup)
		date = pic_content.find("div", {"class": "date"}).getText()
		return date

	@property
	def full_content(self):
		if self.__full_content is not None:
			return self.__full_content

		full_content = self.__parse_full_content()
		self.__full_content = full_content
		return full_content

	def __parse_pic_content(self, soup):
		return soup.find("div", {"class": "piccont"})

	def __parse_title_component(self, soup):
		return soup\
			.find("div", {"class": "blogcont"})\
			.find("h3", {"class": "title"})

	def __parse_full_content(self):
		url = self.url
		soup = conn_utils.get_soup_from_url(url)
		article_description = soup\
			.find("article", {"class": "blogPost"})\
			.find("div", {"class": "description"})
		p_tags = article_description.findAll("p")
		full_content = [p.getText() for p in p_tags]
		full_content = "\n".join(full_content)
		return full_content