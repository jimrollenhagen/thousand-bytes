from setuptools import setup


with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='thousand_bytes',
    packages=['thousand_bytes'],
    include_package_data=True,
    install_requires=requirements,
)
