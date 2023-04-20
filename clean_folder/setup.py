from setuptools import setup, find_packages
import sys

setup(
    name='clean_folder',                    # package name
    version='0.1',                          # version
    description='Package Description',      # short description
    url='http://example.com',               # package URL
    install_requires=[],                    # list of packages this package depends
                                            # on.
    packages=find_packages(),               # List of module names that installing
    script_args=[sys.argv[1]],
    entry_points={
        'console_scripts': [
            'clean-folder=clean_folder.clean:main',
        ],
    }
)
