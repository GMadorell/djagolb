from setuptools import setup, find_packages

version = '0.1.0'

install_requires = []

setup(name='djagolb',
      version=version,
      description="A simple blog made in python for learning purposes.",
      long_description="""\
""",
      classifiers=[],
      keywords='',
      author='',
      author_email='',
      url='',
      license='',
      packages=find_packages(exclude=['tests']),
      include_package_data=True,
      install_requires=install_requires,
      zip_safe=False,
      )
