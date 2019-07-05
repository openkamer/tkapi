from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='tkapi',
    description='Python bindings for the Tweede Kamer OData API',
    long_description=long_description,
    long_description_content_type="text/markdown",
    version='0.8.0.dev3',
    url='https://github.com/openkamer/tkapi',
    author='Open Kamer',
    author_email='info@openkamer.org',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    packages=['tkapi', 'tkapi.util'],
    install_requires=[
        'requests>=2.13.0', 'orderedset>=2.0', 'python-dateutil>=2.0'
    ],
    test_suite="tests",
)
