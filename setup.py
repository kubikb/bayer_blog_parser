from setuptools import setup

setup(name="bayer_blog_parser",
      version='0.1',
      description="A Python plugin to automate the collection of posts from Bayer Zsolt's blog",
      author='Balint Kubik',
      author_email='kubikbalint@gmail.com',
      license='MIT',
      packages=['bayer_blog_parser'],
      install_requires=[],
      test_suite='nose.collector',
      tests_require=['beautifulsoup4', 'joblib', 'nose', 'requests_mock'],
      zip_safe=False)