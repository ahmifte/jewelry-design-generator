#!/usr/bin/env python3
"""
Diagnostic script to help troubleshoot test discovery and coverage issues.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def diagnose_tests():
    """Run various test commands to diagnose issues with test discovery and coverage."""
    # Print environment info
    print('=' * 80)
    print('PYTHON VERSION:')
    subprocess.run([sys.executable, '--version'])
    print('\nPYTHONPATH:')
    print(os.environ.get('PYTHONPATH', 'Not set'))
    print('\nCURRENT DIRECTORY:')
    print(os.getcwd())

    # Check module importability
    print('\n' + '=' * 80)
    print('CHECKING MODULE IMPORTABILITY:')
    try:
        import src.python_jewelry_design_gen
        print('✓ Successfully imported src.python_jewelry_design_gen')
        print(f'Module location: {src.python_jewelry_design_gen.__file__}')
    except ImportError as e:
        print(f'✗ Failed to import src.python_jewelry_design_gen: {e}')

        # Try alternative import
        try:
            import python_jewelry_design_gen
            print('✓ Successfully imported python_jewelry_design_gen')
            print(f'Module location: {python_jewelry_design_gen.__file__}')
        except ImportError as e:
            print(f'✗ Failed to import python_jewelry_design_gen: {e}')

    # Check directory structure
    print('\n' + '=' * 80)
    print('DIRECTORY STRUCTURE:')
    src_path = Path('src/python_jewelry_design_gen')
    tests_path = Path('tests')

    if src_path.exists():
        print(f'✓ {src_path} exists')
        init_file = src_path / '__init__.py'
        if init_file.exists():
            print(f'✓ {init_file} exists')
        else:
            print(f'✗ {init_file} does not exist!')
    else:
        print(f'✗ {src_path} does not exist!')

    if tests_path.exists():
        print(f'✓ {tests_path} exists')
        test_files = list(tests_path.glob('*test*.py'))
        print(f'Found {len(test_files)} test files:')
        for f in test_files:
            print(f'  - {f}')
    else:
        print(f'✗ {tests_path} does not exist!')

    # Run pytest collection only
    print('\n' + '=' * 80)
    print('PYTEST COLLECTION:')
    subprocess.run([
        sys.executable, '-m', 'pytest', '--collect-only', '-v',
    ])

    # Run a single test with high verbosity
    print('\n' + '=' * 80)
    print('RUNNING A BASIC TEST WITH COVERAGE:')
    result = subprocess.run([
        sys.executable, '-m', 'pytest', 'tests/basic_test.py', '-v',
        '--cov=src.python_jewelry_design_gen', '--cov-report=term',
    ])

    if result.returncode != 0:
        print(f'\n✗ Test failed with return code {result.returncode}')
    else:
        print('\n✓ Test passed!')

    return result.returncode


if __name__ == '__main__':
    sys.exit(diagnose_tests())
