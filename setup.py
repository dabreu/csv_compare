from setuptools import setup

setup(name='csv_compare',
      version='0.1',
      description='Simple tool to compare columns of joined rows of two csvs',
      url='http://github.com/alejandrodau/csv_compare',
      author='Alejandro Dau',
      author_email='alejandrodau@gmail.com',
      license='Apache 2.0',
      packages=['csv_compare'],
      entry_points = {
          'console_scripts': ['csv_compare=csv_compare.command_line:main'],
      },
      zip_safe=False)
