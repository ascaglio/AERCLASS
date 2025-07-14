# setup.py - Setup script for installing AERCLASS

from setuptools import setup, find_packages

setup(
    name='aerclass',
    version='1.0.0',
    author='Ariel Scagliotti',
    author_email='your_email@example.com',  # ← cambiar por el real
    description='Aerosol classification and uncertainty analysis toolkit',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ascaglio/AERCLASS',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pandas>=1.3.0',
        'numpy>=1.21.0',
        'matplotlib>=3.4.0',
        'seaborn>=0.11.0'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Atmospheric Science'
    ],
    python_requires='>=3.7'
)