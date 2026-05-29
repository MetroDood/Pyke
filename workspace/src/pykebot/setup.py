from setuptools import find_packages, setup

package_name = 'pykebot'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Metrovods',
    maintainer_email='metrovods@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'Sensor_node = pykebot.Sensor_node:main',
            'Ucracks_node = pykebot.Ucracks_node:main',
            'controller_node = pykebot.Controller_node:main',
        ],
    },
)
