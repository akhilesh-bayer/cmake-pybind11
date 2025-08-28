"""
Setup script for cmakepybind11 package.

This setup.py is designed to work with PEP 621 (pyproject.toml) configuration
while maintaining compatibility with the CMake build system and providing
fallback for legacy build commands.
"""

from setuptools import setup
from setuptools.dist import Distribution
from setuptools.command.install import install


class BinaryDistribution(Distribution):
    """Distribution which always forces a binary package with platform name."""
    
    def has_ext_modules(self):
        return True
    
    def is_pure(self):
        return False


class InstallPlatlib(install):
    """Custom install command to ensure binary packages go to platlib."""
    
    def finalize_options(self):
        install.finalize_options(self)
        self.install_lib = self.install_platlib


if __name__ == "__main__":
    setup(
        distclass=BinaryDistribution,
        cmdclass={'install': InstallPlatlib},
        # PEP 621 metadata is read from pyproject.toml
        # This setup.py only provides build customization
    )
