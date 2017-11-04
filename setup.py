from setuptools import setup
from pypandoc import convert_file

long_description = convert_file('README.md', 'rst')

setup(
    name='tkapi',
    description='Python bindings for the Tweede Kamer OData API',
    long_description=long_description,
    version='0.1.2',
    url='https://github.com/openkamer/tkapi',
    author='Open Kamer',
    author_email='info@openkamer.org',
    license='MIT',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3'
        'License :: OSI Approved :: MIT License',
    ],
    packages=['tkapi'],
    install_requires=[
        'requests>=2.13.0, orderedset>=2.0',
    ],
    test_suite="tests",
)
