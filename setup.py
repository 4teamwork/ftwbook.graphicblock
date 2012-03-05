from setuptools import setup, find_packages
import os


version = '2.1.dev0'
maintainer = 'Jonas Baumann'


tests_require = [
    'zope.testing',
    'plone.app.testing',
    'plone.mocktestcase',
    'ftw.testing',
    ]


setup(name='ftwbook.graphicblock',
      version=version,
      description='Addon for `ftw.book` providing an additional ' + \
          'graphicblock for including PDF documents in the book. ' + \
          '(Maintainer: %s)' % maintainer,
      long_description=open("README.rst").read() + "\n" + \
          open(os.path.join("docs", "HISTORY.txt")).read(),

      classifiers=[
        'Environment :: Web Environment',
        'Framework :: Plone',
        'Framework :: Zope2',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Printing',
        ],

      keywords='ftw book graphicblock pdf',
      author='%s, 4teamwork GmbH' % maintainer,
      author_email='mailto:info@4teamwork.ch',
      maintainer=maintainer,
      url='http://git.4teamwork.ch/',

      license='GPL2',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['ftwbook', ],

      include_package_data=True,
      zip_safe=False,

      install_requires=[
        'setuptools',
        'ftw.book',
        'ftw.pdfgenerator',
        'simplelayout.base',
        ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),

      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
