from distutils.core import setup
import setuptools

setup(name='bratdb',
      version='0.0.6',
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
          'License :: OSI Approved :: MIT License',
      ],
      keywords='nlp information extraction brat',
      entry_points={
          'console_scripts':
              [
                  'bdb-build = bratdb.scripts.build:main',
                  'bdb-freq = bratdb.scripts.freqs:main',
                  'bdb-info = bratdb.scripts.info:main',
                  'bdb-extract = bratdb.scripts.extract:main',
                  'bdb-merge = bratdb.scripts.merge:main',
                  'bdb-extract-build = bratdb.scripts.regexify:main',
                  'bdb-apply = bratdb.scripts.apply:main',
                  'bdb-clean = bratdb.scripts.clean:main',
              ]
      },
      install_requires=['loguru', ],
      package_dir={'': 'src'},
      packages=setuptools.find_packages('src'),
      zip_safe=False
      )
