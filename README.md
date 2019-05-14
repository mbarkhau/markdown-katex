# [markdown-katex][repo_ref]

This is an extension for [Python Markdown](https://python-markdown.github.io/)
which adds [KaTeX](https://katex.org/) support.

Project/Repo:

[![MIT License][license_img]][license_ref]
[![Supported Python Versions][pyversions_img]][pyversions_ref]
[![PyCalVer v201905.0001-alpha][version_img]][version_ref]
[![PyPI Version][pypi_img]][pypi_ref]
[![PyPI Downloads][downloads_img]][downloads_ref]

Code Quality/CI:

[![Build Status][build_img]][build_ref]
[![Type Checked with mypy][mypy_img]][mypy_ref]
[![Code Coverage][codecov_img]][codecov_ref]
[![Code Style: sjfmt][style_img]][style_ref]


|                 Name                |        role       |  since  | until |
|-------------------------------------|-------------------|---------|-------|
| Manuel Barkhau (mbarkhau@gmail.com) | author/maintainer | 2019-05 | -     |


## Install

```bash
$ pip install markdown-katex
```

This package includes the following binaries:

 - `katex-cli-0.10.2-linux-x64`
 - `katex-cli-0.10.2-macos-x64`
 - `katex-cli-0.10.2-win-x64`

If you are on a different platform, or want to use a more recent version of `katex-cli`, you will need to [install it via npm][href_katexinstall_cli].

```bash
$ pip install katex
$ npx katex --version
0.10.2
```

This extension will always use the installed version of katex if it is available.


[repo_ref]: https://gitlab.com/mbarkhau/markdown-katex

[build_img]: https://gitlab.com/mbarkhau/markdown-katex/badges/master/pipeline.svg
[build_ref]: https://gitlab.com/mbarkhau/markdown-katex/pipelines

[codecov_img]: https://gitlab.com/mbarkhau/markdown-katex/badges/master/coverage.svg
[codecov_ref]: https://mbarkhau.gitlab.io/markdown-katex/cov

[license_img]: https://img.shields.io/badge/License-MIT-blue.svg
[license_ref]: https://gitlab.com/mbarkhau/markdown-katex/blob/master/LICENSE

[mypy_img]: https://img.shields.io/badge/mypy-checked-green.svg
[mypy_ref]: https://mbarkhau.gitlab.io/markdown-katex/mypycov

[style_img]: https://img.shields.io/badge/code%20style-%20sjfmt-f71.svg
[style_ref]: https://gitlab.com/mbarkhau/straitjacket/

[pypi_img]: https://img.shields.io/badge/PyPI-wheels-green.svg
[pypi_ref]: https://pypi.org/project/markdown-katex/#files

[downloads_img]: https://pepy.tech/badge/markdown-katex/month
[downloads_ref]: https://pepy.tech/project/markdown-katex

[version_img]: https://img.shields.io/static/v1.svg?label=PyCalVer&message=v201905.0001-alpha&color=blue
[version_ref]: https://pypi.org/project/pycalver/

[pyversions_img]: https://img.shields.io/pypi/pyversions/markdown-katex.svg
[pyversions_ref]: https://pypi.python.org/pypi/markdown-katex

[href_katexinstall_cli]: https://katex.org/docs/cli.html
