
import sys
import subprocess
import pytest

class TestCli:
    def test_1(self):
        ret = subprocess.call(["ansible", "--help"])

        assert ret == 0

    def test_2(self):
        ret = subprocess.call(["ansible-playbook", "--help"])

        assert ret == 0

    def test_3(self):
        ret = subprocess.call(["ansible-galaxy", "collection", "list"])

        assert ret == 0

    def test_4(self):
        ret = subprocess.call(["ansible-galaxy", "role", "list"])

        assert ret == 0

    def test_5(self):
        # Check that we can install a role
        ret = subprocess.call(["ansible-galaxy", "collection", "install", "community.general", "--force"])

        assert ret == 0

    def test_6(self):
        # Check that we can run setup locally
        ret = subprocess.call(["ansible", "-m", "setup", "localhost"])

        assert ret == 0

    def test_7(self):
        # Check that we can run install_deps
        ret = subprocess.call(["/work/bin/install_deps"])

        assert ret == 0

    def test_8(self):
        # Can we run the entrypoint
        ret = subprocess.call(["/work/bin/entrypoint", "ansible-playbook", "--help"])

        assert ret == 0

