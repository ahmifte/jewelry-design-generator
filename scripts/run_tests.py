#!/usr/bin/env python3
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def run_tests():
    """Run the test script with any provided arguments."""
    script_dir = Path(__file__).parent.absolute()
    test_script = script_dir / 'test.sh'

    if not test_script.exists():
        print('Error: test.sh script not found.')
        print('Please make sure it exists in the scripts directory.')
        return 1

    if not os.access(test_script, os.X_OK):
        print('Making test.sh executable...')
        os.chmod(test_script, 0o755)

    args = sys.argv[1:] if len(sys.argv) > 1 else []
    cmd = [str(test_script)] + args

    print(f"Running tests with: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    return result.returncode


if __name__ == '__main__':
    sys.exit(run_tests())
