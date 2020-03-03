from setuptools import setup, find_packages
import os
from setuptools import Command


with open('requirements.txt') as f:
    requirements = f.read().splitlines()


def create_directories():
    directories = ['/var/log/influx-rp-generator/']
    print(f'Start creating directories: {directories}')
    for directory in directories:
        try:
            os.mkdir(directory)
            print(f'{directory} has been created')
        except FileExistsError:
            print(f'{directory} already exist')


def set_permission():
    os.chmod('/etc/init.d/influx-rp-generator', 755)


class CustomInstallCommand(Command):
    user_options = []

    def initialize_options(self):
        """Abstract method that is required to be overwritten"""

    def finalize_options(self):
        """Abstract method that is required to be overwritten"""

    def run(self):
        set_permission()
        create_directories()


tests_require = [],

setup(
    name='influx-rp-generator',
    version='0.0.1',
    description='Influx service to automatically generate RPs',
    url='',
    author='Mykola Kondratiuk',
    author_email='nkondratyk93@gmail.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Programming Language :: Python :: 3.8',
    ],
    setup_requires=[
        'pytest-runner',
        'flake8'
    ],
    keywords='',
    packages=find_packages(),
    install_requires=requirements,
    tests_require=tests_require,
    entry_points={
        'console_scripts': ['influx-rp-generator = rp_generator.__main__:main']
    },
    zip_safe=False,
    include_package_data=True,
    cmdclass={'prepare': CustomInstallCommand},
    data_files=[
        ('/etc/init.d', [
            'data/init-script/influx-rp-generator'
        ])
    ]
)