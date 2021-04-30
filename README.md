
# [markdown-katex][repo_ref]

This is an extension for [Python Markdown](https://python-markdown.github.io/)
which adds [KaTeX](https://katex.org/) support.

    ```math
    f(x) = \int_{-\infty}^\infty
        \hat f(\xi)\,e^{2 \pi i \xi x}
        \,d\xi
    ```

<div align="center">
<p align="center">
<img src="https://raw.githubusercontent.com/mbarkhau/markdown-katex/master/markdown-katex-example.png" height=128>
</p>
</div>

Project/Repo:

[![MIT License][license_img]][license_ref]
[![Supported Python Versions][pyversions_img]][pyversions_ref]
[![CalVer v202103.1029][version_img]][version_ref]
[![PyPI Version][pypi_img]][pypi_ref]
[![PyPI Downloads][downloads_img]][downloads_ref]

Code Quality/CI:

[![GitHub CI Status][github_build_img]][github_build_ref]
[![GitLab CI Status][gitlab_build_img]][gitlab_build_ref]
[![Type Checked with mypy][mypy_img]][mypy_ref]
[![Code Coverage][codecov_img]][codecov_ref]
[![Code Style: sjfmt][style_img]][style_ref]


|                 Name                |        role       |  since  | until |
|-------------------------------------|-------------------|---------|-------|
| Manuel Barkhau (mbarkhau@gmail.com) | author/maintainer | 2019-05 | -     |


## Install

```bash
$ pip install markdown-katex
...
$ python -m markdown_katex --version
markdown-katex version:  v202103.1029 (using binary: /usr/local/bin/npx --no-install katex)
0.13.0
```

This package includes the following binaries:

 - `katex-v0.13.0-x86_64-Linux`
 - `katex-v0.13.0-x86_64-Macos`
 - `katex-v0.13.0-x86_64-Windows`

If you are on a different platform, or want to use a more recent version of `katex-cli`, you will need to [install it via npm][href_katexinstall_cli].

```bash
$ npx katex
$ npx katex --version
0.13.0
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


## Options

 - `no_inline_svg`: Replace inline `<svg>` with `<img data:image/svg+xml;base64..">` tags.
 - `insert_fonts_css`: Insert font loading stylesheet (default: True).


## Development/Testing

```bash
$ git clone https://gitlab.com/mbarkhau/markdown-katex
$ cd markdown-katex
$ make conda
$ make lint mypy test
```


## MkDocs Integration

In your `mkdocs.yml` add this to markdown_extensions.

```yaml
# mkdocs.yml
markdown_extensions:
  - markdown_katex:
      no_inline_svg: True
      insert_fonts_css: True
      macro-file: macros.tex
```

The `macro-file` might looks something like this:

```tex
% macros.tex
\mymacro:\text{prefix #1 suffix}
```

## WeasyPrint Integration

When you generate html that is to be consumed by [WeasyPrint](https://weasyprint.org/), you need to use the `no_inline_svg=True` option. This is due to a [long standing limitation](https://github.com/Kozea/WeasyPrint/issues/75) of WeasyPrint. Without this option, some KaTeX formulas will not render properly, e.g. `\sqrt`

```python
md_ctx = markdown.Markdown(
    extensions=[
        'markdown.extensions.toc',
        'markdown.extensions.extra',
        'markdown.extensions.abbr',
        ...
        'markdown_katex',
    ],
    extension_configs={
        'markdown_katex': {
            'no_inline_svg': True,      # fix for WeasyPrint
            'insert_fonts_css': True,
        },
    }
)
raw_html_text = md_ctx.convert(md_text)
```

You can also use markdown-katex for the conversion of individual formulas from tex to html:

```python
from markdown_katex.extension import tex2html

tex_text = r"""
\frac{1}{\left(\sqrt{\phi\sqrt{5}}-\phi\right)e^{\frac{2}{5}\pi}}=
 1+\frac{e^{-2\pi}} {
   1+\frac{e^{-4\pi}} {
     1+\frac{e^{-6\pi}} {
       1+\frac{e^{-8\pi}} {
         1+\cdots
       }
     }
   }
}
"""
options = {'no_inline_svg': True, 'insert_fonts_css': False}
html = tex2html(tex_text, options)
```


[href_cben_mathdown]: https://github.com/cben/mathdown/wiki/math-in-markdown

[repo_ref]: https://github.com/mbarkhau/markdown-katex

[github_build_img]: https://github.com/mbarkhau/markdown-katex/workflows/CI/badge.svg
[github_build_ref]: https://github.com/mbarkhau/markdown-katex/actions?query=workflow%3ACI

[gitlab_build_img]: https://gitlab.com/mbarkhau/markdown-katex/badges/master/pipeline.svg
[gitlab_build_ref]: https://gitlab.com/mbarkhau/markdown-katex/pipelines

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

[version_img]: https://img.shields.io/static/v1.svg?label=CalVer&message=v202103.1029&color=blue
[version_ref]: https://pypi.org/project/bumpver/

[pyversions_img]: https://img.shields.io/pypi/pyversions/markdown-katex.svg
[pyversions_ref]: https://pypi.python.org/pypi/markdown-katex

[href_katexinstall_cli]: https://katex.org/docs/cli.html

[href_katex_docs]: https://katex.org/docs/supported.html

