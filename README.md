# Parser for Bayer Zsolt's blog
[![Build Status](https://travis-ci.org/kubikb/bayer_blog_parser.svg?branch=master)](https://travis-ci.org/kubikb/bayer_blog_parser)

This repo contains a minimal Python library for parsing posts from the [blog of Bayer Zsolt](https://badog.blogstar.hu), a well-know political publicist in Hungary. I developed it for **Python 2.7** _some time ago_ when I needed a Hungarian text corpus for NLP experiments.

## Usage
The heart of this library is a class named `BayerBlogParser`. Its constructor receives one optional argument: `depth` defines how many pages on the blog should be parsed to collect blog posts. If nothing is provided, all pages (meaning all blog posts) are going to be parsed. Example usage:

```
from bayer_blog_parser.blog_parser import BayerBlogParser
post_data = BayerBlogParser().parse_all_posts()
```

After parsing, `.parse_all_posts()` will return a list of dictionaries with the following keys:
- `url` - The blog post's URL
- `title` - Title
- `author` - Will be Bayer Zsolt most of the time :)
- `lead_text` - The short summary text visible before opening the particular blog post
- `thumbnail_url` - URL of the thumbnail picture
- `date` - Date published
- `full_content` - The full textual content. Paragraphs are separated by newline characters (\n)

You can make a pandas DataFrame from it quite easily: `pd.DataFrame(post_data)`.

For an example, check out `example_parse_all.py`.

## Installation
Just run `python setup.py install`.

## Running the tests
Install dependencies `pip install -r requirements.txt` and execute `nosetests`.