from setuptools import setup, find_packages

setup(name="tornado_fluent", version="0.1.2",
      py_modules=['tornado_fluent'],
      url="http://github.com/sockeye44/tornado_fluent",
      author="Alexander Zelenin",
      author_email='az@inten.to',
      license='bsd',
      python_requires=">=3.3",
      description='Async Fluentd client for Tornado 4-5',
      install_requires=[
          'msgpack-python>=0.4.8',
          'tornado>=4'
      ],
      classifiers = []
)