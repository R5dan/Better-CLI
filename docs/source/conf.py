# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information



project = 'Better CLI'
copyright = '2025, R5dan'
author = 'R5dan'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.napoleon',
              "sphinx.ext.githubpages",
              "sphinx.ext.autosectionlabel",
              "sphinx.ext.autosummary",
              "sphinx_copybutton"]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'Better CLI'
html_theme = 'pydata_sphinx_theme'
html_theme_options = {
    "github_url": "https://github.com/ranaroussi/yfinance",
    "navbar_align": "left"
}
html_static_path = ['_static']
