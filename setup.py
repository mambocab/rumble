try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


readme = open('README.md').read()

requirements = [
    'tabulate',
    'six'
]

test_requirements = [
    'py.test',
    'mock'
]

setup(
    name='simpletimeit',
    version='0.0.4',
    description='A library for easily comparing function runtimes.',
    long_description=readme,
    author='Jim Witschey',
    author_email='jim.witschey@gmail.com',
    url='https://github.com/mambocab/simpletimeit',
    packages=[
        'simpletimeit',
    ],
    package_dir={'simpletimeit':
                 'simpletimeit'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='simpletimeit',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
