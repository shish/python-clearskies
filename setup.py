import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
CHANGES = ""  # open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    #'PyYAML',
    #'BeautifulSoup4',
    #'requests',
    'pyxdg',

    # testing
    'nose',
    'coverage',
    'unittest2',
    'mock',
]

setup(
    name='clearskies',
    version="0.0.0",
    description='A python library for communicating with the ClearSkies daemon',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    author='Shish',
    author_email='shish+clsk@shishnet.org',
    url='https://github.com/shish/python-clearskies',
    keywords='clearskies',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    test_suite='clearskies',
    install_requires=requires,
    entry_points="""\
    [console_scripts]
    cscli = clearskies.cli:main
    """,
)
