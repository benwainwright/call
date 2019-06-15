from setuptools import setup, find_packages

setup(
    name="call",
    version="0.1",
    packages=find_packages(),
    scripts=[
        "call.py"
    ],

    python_requires=">3.7.3",

    install_requires=[
        "aiohttp>=3.5.4",
        "Jinja2>=2.10.1",
        "Click>=7.0"
    ],
    author="Ben Wainwright",
    author_email="bwainwright28@gmail.com"
)
