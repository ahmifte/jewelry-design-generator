from setuptools import setup, find_packages

setup(
    name="python_jewelry_design_gen",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "click",
        "requests",
        "tqdm",
        "python-dotenv",
    ],
    tests_require=[
        "pytest",
        "pytest-cov",
    ],
    entry_points={
        "console_scripts": [
            "jewelry-design-gen=python_jewelry_design_gen.cli:cli",
        ],
    },
)
