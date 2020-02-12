from setuptools import setup, find_packages
import os


version = '3.1.2'
maintainer = 'Jonas Baumann'


tests_require = [
    'zope.testing',
    'plone.app.testing',
    'plone.mocktestcase',
    'ftw.testing<2a',
    'ftw.testbrowser',
    'ftw.builder',
    'ftw.book [tests]',
    ]


setup(name='ftwbook.graphicblock',
      version=version,
      description='Addon for `ftw.book` providing a graphics ' + \
          'block for including PDF documents in the book.',
      long_description=open("README.rst").read() + "\n" + \
          open(os.path.join("docs", "HISTORY.txt")).read(),

      # Get more strings from
      # http://www.python.org/pypi?%3Aaction=list_classifiers

      classifiers=[
        'Framework :: Plone',
        'Framework :: Plone :: 4.3',
        'Framework :: Plone :: 5.1',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],

      keywords='ftw book graphicblock pdf',
      author='4teamwork AG',
      author_email='mailto:info@4teamwork.ch',
      maintainer=maintainer,
      url='https://github.com/4teamwork/ftwbook.graphicblock',

      license='GPL2',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['ftwbook', ],

      include_package_data=True,
      zip_safe=False,

      install_requires=[
        'Plone',
        'setuptools',
        'ftw.book >= 4.0.0',
        'ftw.pdfgenerator',
        'ftw.upgrade',
        ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),

      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
