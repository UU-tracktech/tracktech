from setuptools import setup

setup(name='Auth',
      version='1.0',
      packages=['auth'],
      install_requires=[
          'pyjwt',
          'cryptography'
      ]
      )
