from setuptools import setup

setup(name='initGCProject',
      version='0.1',
      description='Init Project, add necessary file automatically.',
      url='',
      author='Chong Guan',
      author_email='gc771427477@gmail.com',
      license='MIT',
      packages=['initGCProject'],
      scripts=['bin/init'],
      test_suite='nose.collector',
      test_require=['nose'],
      zip_safe=False)
