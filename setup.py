from distutils.core import setup
from catkin_pkg.python_setup import generate_distutils_setup

setup_args = generate_distutils_setup(
    packages=['rqt_mapr'],
    package_dir={'':'src'},
    requires=['std_msgs', 'rospy']
)

setup(**setup_args)