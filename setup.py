
from __future__ import print_function

from os.path import dirname, exists, join
import sys, subprocess
from setuptools import setup

setup_dir = dirname(__file__)
git_dir = join(setup_dir, '.git')
base_package = 'header2whatever'
version_file = join(setup_dir, base_package, 'version.py')

# Automatically generate a version.py based on the git version
if exists(git_dir):
    p = subprocess.Popen(["git", "describe", "--tags", "--long", "--dirty=-dirty"],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    out, err = p.communicate()
    # Make sure the git version has at least one tag
    if err:
        print("Error: You need to create a tag for this repo to use the builder")
        sys.exit(1)

    # Convert git version to PEP440 compliant version
    # - Older versions of pip choke on local identifiers, so we can't include the git commit
    v, commits, local = out.decode('utf-8').rstrip().split('-', 2)
    if commits != '0' or '-dirty' in local:
        v = '%s.post0.dev%s' % (v, commits)

    # Create the version.py file
    with open(version_file, 'w') as fp:
        fp.write("# Autogenerated by setup.py\n__version__ = '{0}'".format(v))

with open(version_file, 'r') as fp:
    exec(fp.read(), globals())

with open(join(setup_dir, 'README.rst'), 'r') as readme_file:
    long_description = readme_file.read()

setup(
    name='header2whatever',
    version=__version__,
    description='Generate files from C/C++ headers using jinja2 templates',
    long_description=long_description,
    author='Dustin Spicuzza',
    author_email='dustin@virtualroadside.com',
    url='https://github.com/virtualroadside/header2whatever',
    keywords='c++ cpp codegen generator header jinja2 template',
    packages=[base_package],
    install_requires=[
        'robotpy-cppheaderparser',
        'jinja2',
        'pyyaml',
        'schematics',
        'pcpp',
    ],
    license='Apache 2.0',
    classifiers=[
        'Operating System :: OS Independent',
        'Environment :: Console',
        'Programming Language :: Python',
        'License :: OSI Approved :: Apache Software License'
    ],
    entry_points = {
        'console_scripts': [
            'h2w = header2whatever.parse:main',
            'h2w-batch = header2whatever.parse:batch'
        ]
    }
    )
