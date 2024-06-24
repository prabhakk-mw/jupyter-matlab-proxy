# Copyright 2024 The MathWorks, Inc.

from tljh_matlab import get_extra_apt_packages_for_matlab as testmodule
import unittest
from unittest import mock
import os


class TestGetExtraAptPackagesForMATLAB(unittest.TestCase):
    extra_apt_packages = [
        "wget",
        "unzip",
        "ca-certificates",
        "xvfb",
        "git",
    ]

    # List of dependencies specifically required for MATLAB R2024a.
    #  This list includes both the basic packages and those specifically needed for MATLAB R2024a on a Ubuntu 22.04 system.
    matlab_deps_for_r2024a = extra_apt_packages + [
        "ca-certificates",
        "libasound2",
        "libc6",
        "libcairo-gobject2",
        "libcairo2",
        "libcap2",
        "libcups2",
        "libdrm2",
        "libfontconfig1",
        "libgbm1",
        "libgdk-pixbuf-2.0-0",
        "libgl1",
        "libglib2.0-0",
        "libgstreamer-plugins-base1.0-0",
        "libgstreamer1.0-0",
        "libgtk-3-0",
        "libice6",
        "libltdl7",
        "libnspr4",
        "libnss3",
        "libpam0g",
        "libpango-1.0-0",
        "libpangocairo-1.0-0",
        "libpangoft2-1.0-0",
        "libsndfile1",
        "libudev1",
        "libuuid1",
        "libwayland-client0",
        "libxcomposite1",
        "libxcursor1",
        "libxdamage1",
        "libxfixes3",
        "libxft2",
        "libxinerama1",
        "libxrandr2",
        "libxt6",
        "libxtst6",
        "libxxf86vm1",
        "locales",
        "locales-all",
        "make",
        "net-tools",
        "procps",
        "sudo",
        "unzip",
        "zlib1g",
    ]

    def test_get_extra_apt_packages_for_matlab(self):
        extra_packages = testmodule.get_extra_apt_packages_for_matlab_impl()
        assert extra_packages == self.matlab_deps_for_r2024a

    def test_get_packages_for_invalid_release(self):
        with mock.patch.dict(os.environ, {"MATLAB_RELEASE": "R2030a"}):
            with self.assertRaises(Exception) as context:
                testmodule.get_extra_apt_packages_for_matlab_impl()

                self.assertTrue(
                    "Invalid Release or OS Specified to fetch matlab-deps"
                    in context.exception
                )


if __name__ == "__main__":
    unittest.main()
