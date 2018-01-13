import logging as log
import requests
from bs4 import BeautifulSoup


def open_url(url):
	log.debug("Opening URL %s..." % url)
	req = requests.get(url)
	status_code = req.status_code
	if status_code < 200 or status_code >= 400:
		error_msg = "Could not open URL (%s)! Status code: %s" %(url, status_code)
		log.error(error_msg)
		raise Exception(error_msg)
	log.debug("Successfully opened URL %s!" % url)
	return req.text

def get_soup_from_page_content(content, parser="html.parser"):
	return BeautifulSoup(content, parser)

def get_soup_from_url(url, parser="html.parser"):
	content = open_url(url)
	soup = get_soup_from_page_content(content, parser)
	log.debug("Successfully obtained BeautifulSoup object from content at URL %s!" % url)
	return soup