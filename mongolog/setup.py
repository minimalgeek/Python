try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Mongo based logger',
    'author': 'Faragó Balázs',
    'author_email': 'farago.balazs87@gmail.com',
    'version': '1.0',
    'packages': ['mongolog'],
    'name': 'mongolog'
}

setup(**config)
