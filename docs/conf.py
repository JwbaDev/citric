"""Sphinx configuration."""
import os

project = "citric"
author = "Edgar Ramírez Mondragón"
copyright = f"2020, {author}"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",
    "autoapi.extension",
]

autoapi_type = "python"
autoapi_root = "_api"
autoapi_dirs = [
    os.path.abspath("../src"),
]
autoapi_options = [
    "members",
    "undoc-members",
    "show-inheritance",
    "show-module-summary",
    "special-members",
    "imported-members",
]
