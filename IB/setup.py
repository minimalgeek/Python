try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

config = {
    'description': 'IB strategies',
    'author': 'Faragó Balázs',
    'url': 'URL to get it at.',
    'download_url': 'Where to download it.',
    'author_email': 'farago.balazs87@gmail.com',
    'version': '0.1',
    'install_requires': required,
    'packages': ['strategies'],
    'scripts': [],
    'name': 'ib-strategies',
    'setup_requires': ['pytest-runner'],
    'tests_require': ['pytest']
}

setup(**config)
