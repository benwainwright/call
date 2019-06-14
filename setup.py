from setuptools import setup, find_packages

setup(
    name="cliapi",
    version="0.1",
    packages=find_packages(),
    scripts=[
        "cliapi.py"
    ],

    install_requires=[
        "aiohttp>=3.5.4",
        "Jinja2>=2.10.1"
    ],
    author="Ben Wainwright",
    author_email="bwainwright28@gmail.com"
)
