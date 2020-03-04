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
    packages=find_packages(),
    version='0.0.2',
    license='Apache License 2.0',
    description='Influx service to automatically generate RPs and switch requests automatically between Grafana and InfluxDB',
    url='https://github.com/howlets/influxdb_downsampling',
    author='Mykola Kondratiuk',
    author_email='howlets.io@gmail.com',
    download_url='https://github.com/howlets/influxdb_downsampling/archive/0.0.2.tar.gz',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.7'
    ],
    setup_requires=[
        'pytest-runner',
        'flake8'
    ],
    keywords=['influxdb', 'grafana', 'downsampling', 'influx proxy'],
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