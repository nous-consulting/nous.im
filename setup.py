from setuptools import setup, find_packages

setup(
    name='nous.im',
    version='0.1',
    description='Instant messanging server controled using xmlrpc.',
    author='Ignas Mikalajunas',
    author_email='ignas@nous.lt',
    url='http://github.com/Ignas/nous.im/',
    classifiers=["Development Status :: 3 - Alpha",
                 "Environment :: Web Environment",
                 "Topic :: Communications :: Email",
                 "Intended Audience :: Developers",
                 "License :: OSI Approved :: GNU General Public License (GPL)",
                 "Programming Language :: Python"],
    install_requires=[
        'mox',
        'zope.testing',
        'PasteDeploy',
        'twisted',
        'wokkel'
        ],
    package_dir={'': 'src'},
    packages=find_packages('src'),
    package_data={'twisted.plugins': ['twisted/plugins/im.py']},
    include_package_data=True,
    zip_safe=False,
    license="GPL",
    entry_points="""
    [console_scripts]
    twistd = twisted.scripts.twistd:run
    """,
)
