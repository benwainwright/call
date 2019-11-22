from setuptools import setup, find_packages

setup(
    name="pycall",
    version="0.1",
    packages=find_packages(),
    scripts=["bin/add-call", "bin/call"],
    python_requires=">3.7.3",
    install_requires=[
        "aiohttp>=3.5.4",
        "jinja2>=2.10.1"
    ],
    author="Ben Wainwright",
    author_email="bwainwright28@gmail.com",
)
