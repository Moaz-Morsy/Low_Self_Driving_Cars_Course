from setuptools import setup

package_name = 'ITI_LAB2'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
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
        "pub=ITI_LAB2.node_1:main",
        "sub_serv=ITI_LAB2.node_2:main",
        "client=ITI_LAB2.node_3:main",
        "reset_turtle=ITI_LAB2.turtle:main"
        ],
    },
)
