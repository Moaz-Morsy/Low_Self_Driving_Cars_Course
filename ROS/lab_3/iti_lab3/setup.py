from setuptools import setup
import os
from glob import glob
package_name = 'iti_lab3'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name), glob('launch/*.launch.py'))
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='moaz',
    maintainer_email='eng.moaz.morsy@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        "my_pub=iti_lab3.node_1:main",
        "my_sub_serv=iti_lab3.node_2:main",
        "my_client=iti_lab3.node_3:main"
        ],
    },
)
