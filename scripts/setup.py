# setup.py

from setuptools import setup, find_packages

setup(
    name='aerclass',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'matplotlib',
        'openpyxl',  # Necesario para leer archivos Excel
    ],
    entry_points={
        'console_scripts': [
            'aerclass = aerclass.main:main'
        ],
    },
)
