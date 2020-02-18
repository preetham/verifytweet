# Verify Tweet verifies tweets of a public user
# from tweet screenshots: real or generated from
# tweet generators.
# Copyright (C) 2019 Preetham Kamidi

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import io
import re

from setuptools import find_packages
from setuptools import setup

with io.open("README.md", "rt", encoding="utf8") as f:
    readme = f.read()

with io.open("verifytweet/__init__.py", "rt", encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)

setup(
    name="verifytweet",
    version=version,
    url="https://preethamkamidi.com/projects/verify",
    project_urls={
        "Documentation": "https://github.com/kamidipreetham/verifytweet",
        "Code": "https://github.com/kamidipreetham/verifytweet",
        "Issue tracker":
        "https://github.com/kamidipreetham/verifytweet/issues",
    },
    license="AGPLv3",
    author="Preetham Kamidi",
    author_email="contact@preethamkamidi.com",
    description="A tool to verify Tweet screenshots",
    long_description=readme,
    long_description_content_type='text/markdown',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.6.*",
    install_requires=[
        "click>=5.1", "Pillow>=6.2.0", "pytesseract==0.2.6",
        "requests==2.22.0", "scikit-learn==0.21.2", "nltk>=3.4.5",
        "python-dateutil==2.8.0", "werkzeug==0.15.4",
        "twint==2.1.13"
    ],
    entry_points={
        "console_scripts": ["verifytweet = verifytweet.cli:run_as_command"]
    },
)