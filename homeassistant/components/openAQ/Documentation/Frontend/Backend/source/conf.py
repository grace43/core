"""Sphinx configuration file for the openAQ sensor file documentation."""

import os
import sys

sys.path.insert(0, os.path.abspath("../../../../"))

project = "openAQ documentation"
copyright_holder = "2023, Group 8"
author = "Group 8"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
]

templates_path = ["_templates"]
exclude_patterns: list = []

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
