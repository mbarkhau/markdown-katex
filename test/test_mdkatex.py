import pytest
import tempfile
import pathlib2 as pl

from markdown import markdown

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

TEX_WITH_SVG_OUTPUT = r"\utilde{AB}"


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
    assert ext.KatexPreprocessor.BLOCK_RE.match(BASIC_BLOCK_TXT)
    alt_block_text = BASIC_BLOCK_TXT.replace("```", "~~~")
    assert ext.KatexPreprocessor.BLOCK_RE.match(alt_block_text)


def test_determinism():
    html_data1 = markdown_katex.tex2html(BASIC_TEX_TXT)
    html_data2 = markdown_katex.tex2html(BASIC_TEX_TXT)
    assert html_data1 == html_data2


def test_tex2html():
    assert len(markdown_katex.TEST_FORMULAS) > 1
    for formula in markdown_katex.TEST_FORMULAS:
        md_text   = "```math\n{0}\n```".format(formula)
        html_text = ext.md_block2html(md_text)
        assert '<span class="katex-display"' in html_text

        md_text   = "$`{0}`$".format(formula)
        html_text = ext.md_inline2html(md_text)
        assert '<span class="katex"' in html_text


def test_basic_block():
    html_data = markdown_katex.tex2html(BASIC_TEX_TXT)

    # with open("debug_output_katex.html", mode="w") as fh:
    #     fh.write(html_data)

    assert '<span class="katex' in html_data

    no_inline_svg  = ext.md_block2html(BASIC_BLOCK_TXT, default_options={'no_inline_svg': False})
    default_output = ext.md_block2html(BASIC_BLOCK_TXT)
    assert no_inline_svg == default_output
    assert default_output
    assert default_output.startswith('<span class="katex-display"')
    expected = "<p>{}</p>".format(default_output)

    result = markdown(BASIC_BLOCK_TXT, extensions=['markdown_katex'])

    assert default_output in result

    assert result.strip().startswith(ext.KATEX_STYLES.strip())
    assert result.endswith(expected)


BASIC_TEX = r"e^{2 \pi i \xi x}"

INLINE_MD_TMPL = """
# Headline

prelude {0} interlude {0}  postscript.
"""


def test_basic_inline():
    inline_txt    = "$`" + BASIC_TEX + "`$"
    inline_output = ext.md_inline2html(inline_txt)
    assert '<span class="katex"' in inline_output

    inline_md_txt = INLINE_MD_TMPL.format(inline_txt)
    result        = markdown(inline_md_txt, extensions=['markdown_katex'])
    assert '<span class="katex"' in result
    assert "Headline" in result
    assert "prelude" in result
    assert "interlude" in result
    assert "postscript" in result
    assert result.count(inline_output) == 2

    assert result.strip().startswith(ext.KATEX_STYLES.strip())


def test_no_svg_inline():
    inline_md_txt = "$`" + TEX_WITH_SVG_OUTPUT + "`$"
    inline_output = ext.md_inline2html(inline_md_txt)
    assert '<span class="katex"' in inline_output
    assert "<svg" in inline_output
    assert "<img" not in inline_output

    inline_output = ext.md_inline2html(inline_md_txt, default_options={'no_inline_svg': True})
    assert '<span class="katex"' in inline_output
    assert "<svg" not in inline_output
    assert "<img" in inline_output

    result = markdown(
        INLINE_MD_TMPL.format(inline_md_txt),
        extensions=['markdown_katex'],
        extension_configs={'markdown_katex': {'no_inline_svg': True}},
    )
    assert '<span class="katex"' in result
    assert "<svg" not in result
    assert "<img" in result


def test_bin_paths():
    assert wrp._get_pkg_bin_path().exists()
    assert wrp._get_pkg_bin_path(machine="x86_64", osname="Windows").exists()
    assert wrp._get_pkg_bin_path(machine="AMD64", osname="Windows").exists()
    assert wrp._get_pkg_bin_path(machine="x86_64", osname="Linux").exists()
    assert wrp._get_pkg_bin_path(machine="x86_64", osname="Darwin").exists()


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

    extensions = DEFAULT_MKDOCS_EXTENSIONS + ['markdown_katex']
    result     = markdown(md_text, extensions=extensions)
    tmp_file = TMP_DIR / "test_output.html"
    with tmp_file.open(mode="w", encoding="utf-8") as fh:
        fh.write(result)
