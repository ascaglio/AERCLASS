# setup.py

from setuptools import setup, find_packages

setup(
    name='aerclass',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'matplotlib',
        'openpyxl',  # Necesario para leer archivos Excel
    ],
    entry_points={
        'console_scripts': [
            'classify_aerosol=aerosol_classification.classification_method_i:classify_aod_ssa',
        ],
    },
)
