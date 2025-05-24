from setuptools import setup, find_packages

setup(
    name='aircraft_indicators',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'matplotlib',
        'numpy',
    ],
    author='egogoboy',
    description='A set of aviation visual indicators for matplotlib: attitude, heading, drift, speed',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='MIT',
    url='https://github.com/egogoboy/aircraft_indicators',
)
