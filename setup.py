import setuptools

setuptools.setup(
    name='Coopy',
    version='0.1',
    author='Adrián Barreal',
    description='Coopy: object oriented constraint programming for Python.',
    packages=setuptools.find_packages(),
    package_dir={'coopy': 'coopy'},
    python_requires='>=3.6'
)