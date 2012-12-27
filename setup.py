from distutils.core import setup

setup(
    name='django-teleport',
    version='0.1',
    packages=['teleport',],
    license='MIT',
    long_description=open('README.rst').read(),
    install_requires=['django',],
)