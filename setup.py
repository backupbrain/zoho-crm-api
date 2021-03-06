import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zohocrmapi",
    version="0.0.11",
    author="Adonis Gaitatzis",
    author_email="backupbrain@gmail.com",
    description="A Zoho CRM API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/backupbrain/zoho-crm-api",
    packages=setuptools.find_packages(),
    install_requires=[
        'requests',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",

    ],
    python_requires='>=3.6',
)
