from setuptools import setup

package_name = 'ninja_turtles'

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
        "add_turtle=ninja_turtles.turtle:main",
        "move=ninja_turtles.move_turtle:main"
        ],
    },
)
