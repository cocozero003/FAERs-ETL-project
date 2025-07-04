from setuptools import setup, find_packages

setup(
    name='faers-etl',
    version='0.1',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'pandas',
        'numpy',
    ],
    entry_points={
        'console_scripts': [
            'run-load-merge=scripts.01_run_load_merge:main',
            'clean-meddra=scripts.02_clean_meddra:main',
            'standardize-demo=scripts.03_standardize_demo:main',
            'map-rxnorm=scripts.04_map_rxnorm:main',
            'create-datasets=scripts.05_create_datasets:main',
        ],
    },
)
