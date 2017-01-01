from setuptools import setup, find_packages

setup(name='gomaticify',
      version='0.1.0',
      description='API for configuring GoCD through YAML file and Gomatic',
      url='https://github.com/DenisTheDilon/gomaticify',
      author='Denis Odilon',
      author_email='dodilon@outlook.com',
      license='MIT',
      packages=find_packages(exclude=("tests",)),
      install_requires=[
          'gomatic',
          'PyYAML'
      ],
      zip_safe=False)
