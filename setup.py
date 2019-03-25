from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='markov_attribution',
      version='0.1',
      description='Marov Channel Attribution',
      long_description='Multi-channel attribution with Markov Chains',
      url='http://github.com/JesseCastro/markov_attribution',
      author='Jesse R. Castro',
      author_email='jesse.r.castro@gmail.com',
      license='MIT',
      packages=['markov_attribution'],
      install_requires=[
        'numpy'
      ],
      include_package_data=True,
      zip_safe=False)
