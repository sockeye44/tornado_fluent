from setuptools import setup, find_packages

setup(name="tornado_fluent", version="0.1",
      py_modules=['urpc'],
      url="http://github.com/sockeye44/tornado_fluent",
      author="Alexander Zelenin",
      author_email='me@sockeye.io',
      license='bsd',
      python_requires=">=3.3",
      description='Async Fluentd client for Tornado 4',
      install_requires=[
          'msgpack-python>=0.4.8',
          'tornado>=4'
      ],
      classifiers = []
)