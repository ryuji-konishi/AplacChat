# This file is used by 'gcloud ml-engine jobs submit' command.
# The following code is required to compose a job package that is uploaded to the cloud.
from setuptools import find_packages
from setuptools import setup

REQUIRED_PACKAGES = []

setup(
    name='nmt',
    version='0.1',
    install_requires=REQUIRED_PACKAGES,
    packages=find_packages(),
    include_package_data=True,
    description='My APLaC chat application package.'
)
