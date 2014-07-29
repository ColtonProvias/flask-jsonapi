"""
Flask-JSONAPI
-------------

JSONAPI View Generators for Flask
"""

from setuptools import setup


setup(name='Flask-JSONAPI',
      version='0.1',
      uri='http://github.com/coltonprovias/flask-jsonapi',
      license='MIT',
      author='Colton J. Provias',
      author_email='cj@coltonprovias.com',
      description='JSONAPI View Generators for Flask',
      long_description=__doc__,
      py_modules=['flask_jsonapi'],
      zip_safe=False,
      include_package_data=True,
      platforms='any',
      install_requires=['Flask', 'SQLAlchemy-JSONAPI'],
      classifiers=['Environment :: Web Environment',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
                   'Topic :: Software Development :: Libraries :: Python '
                   'Modules'])
