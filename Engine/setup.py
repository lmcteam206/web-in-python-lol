from setuptools import setup, find_packages

setup(
    name="web-in-python-lol",
    version="0.1.0",
    description="A lightweight Python-only UI engine for rapid dashboards",
    author="Basel Ezzat",
    packages=find_packages(),
    install_requires=[], # Since you used only standard libs, keep this empty!
)

# python -m build
#python -m twine upload dist/*