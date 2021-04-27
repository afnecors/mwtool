from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="mwtool",
    version='0.1',
    py_modules=['cli'],
    install_requires=requirements,
    entry_points='''
        [console_scripts]
        mwtool=cli:run
    ''',
)