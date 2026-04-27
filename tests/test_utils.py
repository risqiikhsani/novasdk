"""Tests for hypernova-sdk utilities."""

from hypernova_sdk import __version__


def test_version():
    assert __version__ == "1.0.0"
