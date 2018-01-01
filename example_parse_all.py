import logging
import pandas as pd

from bayer_blog_parser.blog_parser import BayerBlogParser

# Setup logging
logging.basicConfig(format='[%(levelname)s] %(asctime)s %(name)s %(filename)s:%(lineno)s - %(message)s',
                    level=logging.DEBUG)

if __name__ == "__main__":
	post_data = BayerBlogParser().parse_all_posts()
	posts_df = pd.DataFrame(post_data)
	posts_df.to_csv("data/posts.tsv", sep="\t", encoding="utf-8", index=False)