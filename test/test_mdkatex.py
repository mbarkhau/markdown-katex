# -*- coding: utf-8 -*-
# This file is part of markdown-katex.
# https://gitlab.com/mbarkhau/markdown-katex
#
# Copyright (c) 2019-2021 Manuel Barkhau (mbarkhau@gmail.com) - MIT License
# SPDX-License-Identifier: MIT

# pytest fixtures work this way
# pylint: disable=redefined-outer-name
# for wrp._get_pkg_bin_path
# pylint: disable=protected-access

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import io
import re
import tempfile
import textwrap
from xml.etree.ElementTree import XML

import bs4
import pytest
import markdown as md
import pathlib2 as pl

import markdown_katex
import markdown_katex.wrapper as wrp
import markdown_katex.extension as ext

DATA_DIR = pl.Path(__file__).parent.parent / "fixture_data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

TMP_DIR = pl.Path(tempfile.gettempdir()) / "mdkatex"

BASIC_TEX_TXT = r"""
f(x) = \int_{-\infty}^\infty
    \hat f(\xi)\,e^{2 \pi i \xi x}
    \,d\xi
"""

TEX_WITH_SVG_OUTPUT = "\\utilde{AB}"


BASIC_BLOCK_TXT = "```math\n" + BASIC_TEX_TXT + "```"


DEFAULT_MKDOCS_EXTENSIONS = ['meta', 'toc', 'tables', 'fenced_code']


EXTENDED_BLOCK_TXT = r"""
# Heading

prelude

```math
{0}
```

postscript
"""


EXTENDED_HTML_TEMPLATE = r"""
<h1 id="heading">Heading</h1>
<p>prelude</p>
<p>{0}</p>
<p>postscript</p>
"""


@pytest.fixture()
def katex_output():
    path = DATA_DIR / "katex_output.html"
    with path.open(mode="r") as fobj:
        return fobj.read()


def test_svg2img(katex_output):
    assert "<svg" in katex_output
    assert "</svg>" in katex_output

    assert "<img" not in katex_output

    result = ext.svg2img(katex_output)

    assert "<img" in result

    out_path = DATA_DIR / "katex_output_no_inline_svg.html"
    with out_path.open(mode="w") as fobj:
        fobj.write(result)


def test_regexp():
    block_texts = [
        BASIC_BLOCK_TXT,
        BASIC_BLOCK_TXT.replace("```", "~~~"),
        BASIC_BLOCK_TXT.replace("```", "~~~~"),
        BASIC_BLOCK_TXT.replace("```", "````"),
    ]

    for block_text in block_texts:
        assert ext.BLOCK_START_RE.match(block_text)
        assert ext.BLOCK_CLEAN_RE.match(block_text)


INLINE_TEST_CASES = {
    "1 pre `a+b` post"     : [],
    "2 pre $`a+b` post"    : [],
    "3 pre `a+b`$ post"    : [],
    "4 pre $`a+b`$ post"   : ["$`a+b`$"],
    "5 pre $``a+b``$ post" : ["$``a+b``$"],
    "6 pre``$`a+b`$`` post": [],
    "7 pre``$`a+b`$`` post": [],
    # multimatch
    "1 pre $a+b`$ inter $c+d`$  post"      : [],
    "2 pre $`a+b`$ inter $`c+d`$  post"    : ["$`a+b`$", "$`c+d`$"],
    "3 pre $``a+b``$ inter $``c+d``$  post": ["$``a+b``$", "$``c+d``$"],
}


@pytest.mark.parametrize("line, expected", INLINE_TEST_CASES.items())
def test_inline_parsing(line, expected):
    result = [code_item.inline_text for code_item in ext.iter_inline_katex(line)]
    assert result == expected


def test_inline_multiple():
    md_text = """
    # headline

    Pre $`a+b`$ inter 1 $`c+d`$ inter 2 $`e+f`$ post
    """
    md_text = textwrap.dedent(md_text)
    result  = md.markdown(md_text, extensions=['markdown_katex'])
    assert "md_katex" not in result
    assert result.strip().startswith(ext.KATEX_STYLES.strip())
    # check that spans were added
    assert result.count('<span class="katex"><') == 3
    # check that markers were replaced
    assert '<span class="katex">katex' not in result


def test_determinism():
    html_data1 = markdown_katex.tex2html(BASIC_TEX_TXT)
    html_data2 = markdown_katex.tex2html(BASIC_TEX_TXT)
    assert html_data1 == html_data2


def test_tex2html():
    assert len(markdown_katex.TEST_FORMULAS) > 1
    for formula in markdown_katex.TEST_FORMULAS:
        md_text   = "```math\n{0}\n```".format(formula)
        html_text = ext.md_block2html(md_text)
        assert html_text.startswith('<span class="katex-display"')
        assert html_text.endswith("</span>")

        md_text   = "$`{0}`$".format(formula)
        html_text = ext.md_inline2html(md_text)
        assert html_text.startswith('<span class="katex"')
        assert html_text.endswith("</span>")


def test_basic_block():
    html_data = markdown_katex.tex2html(BASIC_TEX_TXT)

    # with open("debug_output_katex.html", mode="w") as fobj:
    #     fobj.write(html_data)

    assert '<span class="katex' in html_data

    no_inline_svg  = ext.md_block2html(BASIC_BLOCK_TXT, default_options={'no_inline_svg': False})
    default_output = ext.md_block2html(BASIC_BLOCK_TXT)
    assert no_inline_svg == default_output
    assert default_output
    assert default_output.startswith('<span class="katex-display"')
    expected = "<p>{}</p>".format(default_output)

    result = md.markdown(BASIC_BLOCK_TXT, extensions=['markdown_katex'])
    assert "md_katex" not in result

    assert default_output in result

    assert result.strip().startswith(ext.KATEX_STYLES.strip())
    assert result.endswith(expected)


def test_block_styles():
    assert "```" in BASIC_BLOCK_TXT

    html_data = ext.md_block2html(BASIC_BLOCK_TXT)
    assert '<span class="katex' in html_data
    html_data = ext.md_block2html(BASIC_BLOCK_TXT.replace("```", "````"))
    assert '<span class="katex' in html_data
    html_data = ext.md_block2html(BASIC_BLOCK_TXT.replace("```", "~~~~"))
    assert '<span class="katex' in html_data
    html_data = ext.md_block2html(BASIC_BLOCK_TXT.replace("```", "~~~"))
    assert '<span class="katex' in html_data


BASIC_TEX = r"e^{2 \pi i \xi x}"

INLINE_MD_TMPL = """
# Headline

prelude {0} interlude {1}  postscript.
"""


def test_inline_basic():
    inline_txt    = "$`" + BASIC_TEX + "`$"
    inline_output = ext.md_inline2html(inline_txt)
    assert '<span class="katex"' in inline_output

    inline_md_txt = INLINE_MD_TMPL.format(inline_txt, inline_txt)
    result        = md.markdown(inline_md_txt, extensions=['markdown_katex'])
    assert "md_katex" not in result

    assert '<span class="katex"' in result
    assert "Headline" in result
    assert "prelude" in result
    assert "interlude" in result
    assert "postscript" in result
    assert result.count(inline_output) == 2

    assert result.strip().startswith(ext.KATEX_STYLES.strip())


def test_trailing_whitespace():
    default_output = ext.md_block2html(BASIC_BLOCK_TXT)

    trailing_space_result = md.markdown(BASIC_BLOCK_TXT + "  ", extensions=['markdown_katex'])
    assert "md_katex" not in trailing_space_result
    assert default_output in trailing_space_result
    assert "```" not in trailing_space_result


def test_inline_quoted():
    inline_txt        = "$`" + BASIC_TEX + "`$"
    quoted_inline_txt = "``$`" + BASIC_TEX + "`$``"
    inline_output     = ext.md_inline2html(inline_txt)

    inline_md_txt = INLINE_MD_TMPL.format(inline_txt, quoted_inline_txt)
    result        = md.markdown(inline_md_txt, extensions=['markdown_katex'])
    assert "md_katex" not in result
    assert result.count(inline_output) == 1
    assert "span id=\"katex" not in result

    inline_md_txt = INLINE_MD_TMPL.format(quoted_inline_txt, inline_txt)
    result        = md.markdown(inline_md_txt, extensions=['markdown_katex'])
    assert "md_katex" not in result
    assert result.count(inline_output) == 1
    assert "span id=\"katex" not in result


def test_marker_uniqueness():
    inline_md_txt = "\n\n".join(
        ["start", "$`a+b`$", "interlude", "$``c+d``$", "interlude", "$``a+b``$", "end"]
    )
    md_ctx  = md.Markdown(extensions=['markdown_katex'])
    preproc = next(
        iter((pp for pp in md_ctx.preprocessors if isinstance(pp, ext.KatexPreprocessor)))
    )
    out_lines = preproc.run(inline_md_txt.splitlines())
    md_output = "\n".join(out_lines)

    assert md_output.count("tmp_inline_md_katex") == 3
    marker_ids = [match.group(1) for match in re.finditer(r"tmp_inline_md_katex_(\d+)", md_output)]
    assert len(set(marker_ids)) == 2


def test_svg_uniqueness():
    md_text = "\n\n".join(
        [
            "start",
            "$`a+b`$",
            "interlude",
            "$`c+d`$",
            "interlude",
            "```math\na+b\n```",
            "interlude",
            "```math\ne+f\n```",
            "interlude",
            "```math\na+b\n```",
            "interlude",
            "prefix $`a+b`$ suffix",
            "end",
        ]
    )
    html_output = md.markdown(md_text, extensions=['markdown_katex'])
    assert "md_katex" not in html_output

    # check whitespace
    assert "prefix <span " in html_output
    assert "</span> suffix" in html_output

    fobj = io.StringIO(html_output)
    soup = bs4.BeautifulSoup(fobj, "html.parser")

    results = set()
    for tag in soup.find_all("span", attrs={'class': "katex"}):
        results.add(str(tag))

    assert len(results) == 4


def test_no_inline_svg():
    inline_md_txt = "$`" + TEX_WITH_SVG_OUTPUT + "`$"
    inline_output = ext.md_inline2html(inline_md_txt)
    assert '<span class="katex"' in inline_output
    assert "<svg" in inline_output
    assert "<img" not in inline_output

    inline_output = ext.md_inline2html(inline_md_txt, default_options={'no_inline_svg': True})
    assert '<span class="katex"' in inline_output
    assert "<svg" not in inline_output
    assert "<img" in inline_output

    result = md.markdown(
        INLINE_MD_TMPL.format(inline_md_txt, inline_md_txt),
        extensions=['markdown_katex'],
        extension_configs={'markdown_katex': {'no_inline_svg': True}},
    )
    assert "md_katex" not in result
    assert '<span class="katex"' in result
    assert "<svg" not in result
    assert "<img" in result


def test_insert_fonts_css():
    result = md.markdown(
        BASIC_BLOCK_TXT,
        extensions=['markdown_katex'],
        extension_configs={'markdown_katex': {'insert_fonts_css': True}},
    )
    assert "md_katex" not in result
    assert result.startswith(ext.KATEX_STYLES.strip())
    result = md.markdown(
        BASIC_BLOCK_TXT,
        extensions=['markdown_katex'],
        extension_configs={'markdown_katex': {'insert_fonts_css': False}},
    )
    assert "md_katex" not in result
    assert not result.startswith(ext.KATEX_STYLES.strip())


def test_err_msg():
    invalid_md_txt = r"$`e^{2 \pi i \xi x`$"
    md_txt         = INLINE_MD_TMPL.format(invalid_md_txt, invalid_md_txt)
    try:
        md.markdown(md_txt, extensions=['markdown_katex'])
        assert False, "expected an exception"
    except wrp.KatexError as err:
        err_msg = err.args[0]
        assert "ParseError: KaTeX parse error:" in err_msg
        assert "Expected '}'" in err_msg


def test_bin_paths():
    assert wrp._get_pkg_bin_path().exists()
    assert wrp._get_pkg_bin_path(machine="x86_64", osname="Windows").exists()
    assert wrp._get_pkg_bin_path(machine="AMD64", osname="Windows").exists()
    assert wrp._get_pkg_bin_path(machine="x86_64", osname="Linux").exists()
    assert wrp._get_pkg_bin_path(machine="x86_64", osname="Darwin").exists()
    assert str(wrp._get_pkg_bin_path(machine="AMD64", osname="Windows")).endswith(".exe")


def test_html_output():
    # NOTE: This generates html that is to be tested
    #   in the browser (for warnings in devtools).
    assert len(markdown_katex.TEST_FORMULAS) > 1
    md_parts = []
    for formula in markdown_katex.TEST_FORMULAS:
        inline_formula = formula.replace("\n", " ").strip()
        md_parts.append("Inline: $`" + inline_formula + "`$")
        md_parts.append("\n\n---\n\n```math" + formula + "\n```")

    md_text = "# Headline\n\n" + "\n".join(md_parts)
    result  = md.markdown(
        md_text,
        extensions=DEFAULT_MKDOCS_EXTENSIONS + ['markdown_katex'],
        extension_configs={'markdown_katex': {'no_inline_svg': True}},
    )
    assert "md_katex" not in result
    html = """
    <html>
    <head>
        <style>
        body {
            background: white;
        }
        @media print {
            @page {
                /* A4 - landscape */
                padding: 0;
                margin: 20mm;
                size: 297mm 210mm;
            }
        }
        </style>
    </head>
    <body>
    {{result}}
    </body>
    </html>
    """
    html = textwrap.dedent(html.lstrip("\n"))
    html = html.replace("{{result}}", result)

    tmp_file = TMP_DIR / "test_output.html"
    with tmp_file.open(mode="w", encoding="utf-8") as fobj:
        fobj.write(html)


def test_valid_xml():
    md_text = textwrap.dedent(
        r"""
        Look at these formulas:

        ```math
        f(x) = 0
        ```
        """
    )

    extensions = DEFAULT_MKDOCS_EXTENSIONS + ['markdown_katex']
    result     = md.markdown(
        md_text,
        extensions=extensions,
        extension_configs={'markdown_katex': {'no_inline_svg': True}},
    )

    # avoid xml.etree.ElementTree.ParseError: junk after document element:
    # XML expects a single root object containing all the others
    result = "<div>" + result + "</div>"

    # assert no exception
    XML(result)


def test_ignore_in_non_math_block():
    md_text = textwrap.dedent(
        r"""
        Look at these formulas:

        ```
        This math is in a block $`a^2+b^2=c^2`$.
        ```

        And also this code:

        ```python
        def randint() -> int:
            return 4
        ```

        And this code:

        ~~~javascript
        function randint() {
            return 4;
        }
        ~~~
        """
    )
    result_a = md.markdown(
        md_text,
        extensions=DEFAULT_MKDOCS_EXTENSIONS + ['markdown_katex'],
        extension_configs={'markdown_katex': {'no_inline_svg': True}},
    )
    result_b = md.markdown(
        md_text,
        extensions=DEFAULT_MKDOCS_EXTENSIONS,
    )
    assert "md_katex" not in result_a
    assert "md_katex" not in result_b
    assert "katex" not in result_a
    assert "katex" not in result_b

    assert result_a == result_b
    assert "<pre><code>This math is in" in result_a
    assert re.search(r'<pre><code class="(language-)?python">def randint', result_a)
    assert re.search(r'<pre><code class="(language-)?javascript">function randint', result_a)


def test_macro_file():
    md_text = textwrap.dedent(
        """
        prelude
        ```math
        \\macroname{aaaAAA}{bbbBBB}
        ```
        postscript
        """
    )
    macro_text = textwrap.dedent(
        """
        % macros.tex
        \\macroname:\\text{prefix} \\text{#2} \\text{interlude} \\text{#1} \\text{suffix}
        """
    )

    with tempfile.NamedTemporaryFile(suffix=".tex") as fobj:
        fobj.write(macro_text.encode("ascii"))
        fobj.flush()

        macro_file = fobj.name

        result = md.markdown(
            md_text,
            extensions=DEFAULT_MKDOCS_EXTENSIONS + ['markdown_katex'],
            extension_configs={'markdown_katex': {'no_inline_svg': True, 'macro-file': macro_file}},
        )
        assert "md_katex" not in result
        assert "prefix" in result
        assert "interlude" in result
        assert "suffix" in result
        assert result.index("bbbBBB") < result.index("aaaAAA")


def test_md_in_html():
    md_text = textwrap.dedent(
        """
        <div markdown="1">
        ```math
        a^2+b^2=c^2
        ```

        $`a^3+b^3=c^3`$
        </div>
        """
    )
    result = md.markdown(
        md_text,
        extensions=DEFAULT_MKDOCS_EXTENSIONS + ['markdown_katex', 'extra'],
        extension_configs={'markdown_katex': {'no_inline_svg': True}},
    )
    assert "md_katex" not in result
    assert '<span class="katex-display">' in result
    assert '<span class="katex">' in result


ADMONITON_FIXTURE = """
Prelude

!!! hint
    A block formula

    ````math
    \\begin{gather}
     sin(x)
    \\end{gather}
    ````

    An inline $`a^3+b^3=c^3`$ formula.

Postscript
"""


def test_admonition():
    result = md.markdown(
        ADMONITON_FIXTURE,
        extensions=DEFAULT_MKDOCS_EXTENSIONS + ['markdown_katex', 'extra', 'admonition'],
        extension_configs={'markdown_katex': {'no_inline_svg': True}},
    )

    assert "md_katex" not in result
    assert '<span class="katex-display">' in result
    assert '<span class="katex">' in result

    # is the katex inside the admonition ?
    assert result.count('<div class="admonition ') == 1
    assert result.index('<span class="katex-display">') > result.index('<div class="admonition ')
    assert result.index('<span class="katex-display">') < result.index("</div>")
