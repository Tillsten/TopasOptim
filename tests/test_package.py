from __future__ import annotations

import importlib.metadata

import topasoptim as m


def test_version():
    assert importlib.metadata.version("topasoptim") == m.__version__
