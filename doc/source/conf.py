# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

# Add this near the top of conf.py
import os
import sys
sys.path.insert(0, os.path.abspath("../.."))


project = "Better CLI"
copyright = "2025, R5dan"
author = "R5dan"
release = "0.1.0"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.githubpages",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.autosummary",
    "sphinx_design",
    "sphinx_copybutton",
    "pydata_sphinx_theme",
    ]

templates_path = ["_templates"]
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output


# Material theme options
html_theme = "pydata_sphinx_theme"

# Theme options
html_theme_options = {
}

html_static_path = ["_static"]
templates_path = ['_templates']

