
# [markdown-katex][repo_ref]

This is an extension for [Python Markdown](https://python-markdown.github.io/)
which adds [KaTeX](https://katex.org/) support.

    ```math
    f(x) = \int_{-\infty}^\infty
    \hat f(\xi)\,e^{2 \pi i \xi x}
    \,d\xi
    ```

<p align="center">
<img src="https://mbarkhau.keybase.pub/static/markdown-katex-example.png" height=128>
</p>

Project/Repo:

[![MIT License][license_img]][license_ref]
[![Supported Python Versions][pyversions_img]][pyversions_ref]
[![PyCalVer v201910.0010-beta][version_img]][version_ref]
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

This extension will always use the locally installed version of KaTeX if it is available, instead of using the implementation bundled with this package.

No JavaScript is required to render the resulting HTML, so it can be used with more limited renderers (which don't support JavaScript) such as [WeasyPrint](https://weasyprint.org/) .


## Usage

Formulas can be created and edited interactively using the editor on [katex.org](https://katex.org/). They also have some [good documentation][href_katex_docs] for the subset of LaTeX that is supported. When embedding these in your Markdown files, they must be marked with a special syntax in order to be rendered using KaTeX. There are [many syntax extensions][href_cben_mathdown] for Markdown that allow LaTeX formulas to be embedded, however this package only supports the syntax introduced by Gitlab:

 - For inline mode formulas: &dollar;&#96;...&#96;&dollar; 
 - For display mode formulas: &#96;&#96;&#96;math

Here is [an example](https://gitlab.com/snippets/1857641) that uses this syntax.

There are two main advantages of this syntax:

 1. Gitlab has an existing Markdown renderer that can be used without the need to download any software. This implementation also uses KaTeX, so the output should be exactly the same as this extension.
 2. The fallback behaviour of other Markdown renderers is to render the raw LaTeX as inline code or a code block. This means that they won't inadvertently parse a LaTeX formula as Markdown syntax.

Hopefully other renderers will also adopt support for this syntax as:

 1. Rendering is done in the browser using KaTeX so implementation effort and should be minimal.
 2. The false positive rate for existing Markdown documents is negligible (ie. existing alternate use of &dollar;&#96; syntax is minimal to non-existent).


## Development/Testing

```bash
$ git clone https://gitlab.com/mbarkhau/markdown-katex
$ cd markdown-katex
$ make install
$ make lint mypy test
```



## MkDocs Integration

In your `mkdocs.yml` add this to markdown_extensions.

```yaml
markdown_extensions:
  - markdown_katex:
      no_inline_svg: True
```


[href_cben_mathdown]: https://github.com/cben/mathdown/wiki/math-in-markdown

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

[version_img]: https://img.shields.io/static/v1.svg?label=PyCalVer&message=v201910.0010-beta&color=blue
[version_ref]: https://pypi.org/project/pycalver/

[pyversions_img]: https://img.shields.io/pypi/pyversions/markdown-katex.svg
[pyversions_ref]: https://pypi.python.org/pypi/markdown-katex

[href_katexinstall_cli]: https://katex.org/docs/cli.html

[href_katex_docs]: https://katex.org/docs/supported.html

