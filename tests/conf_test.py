from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

src_path = Path(__file__).parent.parent / 'src'
sys.path.insert(0, str(src_path.absolute()))


def pytest_addoption(parser):
    """Add command-line options for testing."""
    parser.addoption(
        '--batch-size',
        action='store',
        default='3',
        help='Batch size to use for tests (default: 3)',
    )


@pytest.fixture(scope='session')
def batch_size(request):
    return int(request.config.getoption('--batch-size'))


@pytest.fixture(autouse=True)
def env_setup():
    old_env = os.environ.copy()
    os.environ['MESHY_API_KEY'] = 'test-key-for-unit-tests'

    yield

    # Restore original environment
    os.environ.clear()
    os.environ.update(old_env)
