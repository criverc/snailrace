import os
from setuptools import setup

setup (name="snailrace",
       version="0.1",
       scripts=[ 'snailrace.py' ],
       packages=['snailracerc'],
       install_requires=['pygame'],
       package_data={ 'snailracerc' : ['*.gif', '*.ogg'] })
