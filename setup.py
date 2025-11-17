from setuptools import setup, find_packages

setup(
    name='wconfig',
    version="1.0",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'wconfig=wconfig.main:main',
        ],
    },
    install_requires=[
        'rich',
        'Pygments',
        'mdurl',
        'markdown-it-py',
    ],
)
