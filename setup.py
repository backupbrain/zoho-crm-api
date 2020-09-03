import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zohocrmapi-backupbrain",
    version="0.0.1",
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
        "License :: OSI Approved :: GPL License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
