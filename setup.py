from setuptools import setup

setup(
      name='file_processor',
      version='1.0',
      description='Provides function read_file() to read fixed ascii files',
      long_description=open('README.md').read(),
      author='Unterbusch Simon',
      license='MIT License ',
      packages=['file_processor'],
      install_requires=[
          'numpy>=1.18.0',
          'pandas>=1.0'
      ], classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6'],
      include_package_data=True,
      package_dat={'Schema': ["/Schema/*/*/*/*.csv"], 'data': ["/data/*.dat"]},
      zip_safe=False
)
