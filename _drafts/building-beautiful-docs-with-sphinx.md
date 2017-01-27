# Building Beautiful Documentation with Sphinx

two of the [resolutions](http://blog.districtdatalabs.com/ten-things-to-try-in-2017) - be a better software engineer (e.g. documentation) and more adventures in open source! link to ddl post. 2 birds with one stone


## What is Yellowbrick?

[Yellowbrick](https://github.com/DistrictDataLabs/yellowbrick) is suite of visual analysis and diagnostic tools to facilitate feature selection, model selection, and parameter tuning for machine learning.


### What is MkDocs?

MkDocs is a software documentation tool written in Markdown that can be hosted on ReadTheDocs.org.
See [MkDocs](http://www.mkdocs.org/) for document generation in Markdown that Read the Docs will render. Read the Docs allows you to connect a Github repository so that whenever you push new code (and new documentation), it is automatically built and updated on the website. Read the Docs can even maintain different versions of documentation for different releases.


### What is Sphinx?

[reStructuredText Primer](http://sphinx-doc.org/rest.html)


### What is reStructuredText?

[reStructuredText](http://docutils.sourceforge.net/rst.html) is an easy-to-read plaintext markup syntax specifically designed for use in Python docstrings or to generate Python documentation. In fact, the reStructuredText parser is a component of [Docutils](http://docutils.sourceforge.net/), an open-source text processing system that is used by [Sphinx](http://sphinx-doc.org/) to generate intelligent and beautiful software documentation, in particular the native Python documentation.

To learn more about reStructuredText syntax, please see the [reStructuredText Primer](http://sphinx-doc.org/rest.html).

why we decided to use sphinx instead of mkdocs

mention ben post on documentation:
http://blog.districtdatalabs.com/markup-for-fast-data-science-publication


## Getting started with Sphinx

```bash
$ pip install -U Sphinx
```

As of the time of this writing, the current version of Sphinx is 1.5.1, and the installation includes the following dependencies:

 - babel-2.3.4
 - Jinja2-2.8.1
 - pytz-2016.10
 - docutils-0.13.1
 - alabaster-0.7.9
 - imagesize-0.7.1
 - requests-2.12.4
 - snowballstemmer-1.2.1

Also have to install the ReadTheDocs theme for Sphinx:

```bash
$ pip install sphinx_rtd_theme
```

use Sphinx to generate reStructuredText documentation for your apps and libraries in a `docs` directory at the top-level:

```bash
$ mkdir docs
$ cd docs
$ sphinx-quickstart
```

The quickstart command line utility will then ask a [series of configuration questions](https://pythonhosted.org/an_example_pypi_project/sphinx.html), to which you can enter custom answers or just press **Enter** to accept the default value given in brackets. The custom answers I included were:

```bash
...
> Project name: # type your project name
> Author name(s): # type your name
> Project version []: # type project version
...
> autodoc: automatically insert docstrings from modules (y/n) [n]: # type y
...
> intersphinx: link between Sphinx documentation of different projects (y/n) [n]:
> todo: write "todo" entries that can be shown or hidden on build (y/n) [n]: y
> coverage: checks for documentation coverage (y/n) [n]: y
...
> mathjax: include math, rendered in the browser by MathJax (y/n) [n]: y
```

Similar to iPython Notebook, reStructured text can render LaTeX syntax mathematical formulae. This utility will create a Makefile for you; to generate HTML documentation, simply run the following command in the `docs` directory:

```bash
$ make html
```

The output will be built, and you can view `_build/html/index.html` in your browser.
