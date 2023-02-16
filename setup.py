from setuptools import setup

README = ''
with open('README.md', 'r', encoding='utf-8') as readme_file:
    README = readme_file.read()

setup(
    name='seo-keyword-research-tool',
    description = 'Python SEO keywords suggestion tool. Google Autocomplete, Related Questions and Related Searches.',
    url='https://github.com/chukhraiartur/seo-keyword-research-tool',
    version='0.1.1',
    license='MIT',
    author='Artur Chukhrai',
    author_email='chukhraiartur@gmail.com',
    maintainer='Artur Chukhrai, Dmitiry Zub',
    maintainer_email='chukhraiartur@gmail.com, dimitryzub@gmail.com',
    long_description_content_type='text/markdown',
    long_description=README,
    include_package_data=True,
    python_requires='>=3.8',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
        'Topic :: Internet',
        'Natural Language :: English',
        'Topic :: Utilities',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    keywords=[
        'google scholar',
        'serpapi',
        'scraper',
        'python',
        'python google scholar',
        'python google scholar api',
        'web scraping',
        'python web scraping',
        'research',
        'google-search-results',
        'cli'
    ],
    install_requires=[
          'google-search-results>=2.4',
    ],
    project_urls={
        'Documentation': 'https://github.com/chukhraiartur/seo-keyword-research-tool',
        'Source': 'https://github.com/chukhraiartur/seo-keyword-research-tool',
        'Tracker': 'https://github.com/chukhraiartur/seo-keyword-research-tool/issues',
    },
)