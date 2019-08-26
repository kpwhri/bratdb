from distutils.core import setup
import setuptools

setup(name='bratdb',
      version='0.0.1',
      description='Extract brat-formatted data to prepare the annotated data for various NLP applications',
      url='https://github.com/kpwhri/bratdb',
      author='dcronkite',
      author_email='dcronkite@gmail.com',
      license='MIT',
      classifiers=[  # from https://pypi.python.org/pypi?%3Aaction=list_classifiers
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Science/Research',
          'Programming Language :: Python :: 3 :: Only',
          'Topic :: Text Processing :: Linguistic',
      ],
      keywords='nlp information extraction brat',
      entry_points={
          'console_scripts':
              [
                  'bdb-build = bratdb.scripts.build:main',
              ]
      },
      install_requires=['loguru', ],
      package_dir={'': 'src'},
      packages=setuptools.find_packages('src'),
      zip_safe=False
      )
