from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='Products.zhkath',
      version=version,
      description="Theme and Features for zh.kath.ch",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='',
      author='',
      author_email='',
      url='http://svn.plone.org/svn/collective/',
      license='GPL',
      namespace_packages=['Products'],
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'Products.feedfeeder'
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
