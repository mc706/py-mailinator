from setuptools import setup

import re
VERSIONFILE="pymailinator/_version.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
    major, minor, patch = verstr.split('.')
    release = "%s.%s" %(major, minor)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))
# Setup
setup(
    name='py-mailinator',
    version=verstr,
    url='https://github.com/mc706/py-mailinator',
    author='Ryan McDevitt',
    author_email='mcdevitt.ryan@gmail.com',
    license='MIT License',
    packages=['pymailinator'],
    include_package_data=True,
    description='Python API wrapper for mailinator',
    download_url = 'https://github.com/mc706/py-mailinator/tarball/' + release,
    keywords = ['mailinator', 'api', 'email'],
    classifiers = [],
)