# This file is part of the markdown-katex project
# https://gitlab.com/mbarkhau/markdown-katex
#
# Copyright (c) 2019 Manuel Barkhau (mbarkhau@gmail.com) - MIT License
# SPDX-License-Identifier: MIT
import re
import json
import base64
import logging
import typing as typ

from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from markdown.postprocessors import Postprocessor

import markdown_katex.wrapper as wrapper


log = logging.getLogger(__name__)


SVG_ELEM_RE = re.compile(r"<svg.*?</svg>", flags=re.MULTILINE | re.DOTALL)

SVG_XMLNS = 'xmlns="http://www.w3.org/2000/svg" ' + 'xmlns:xlink="http://www.w3.org/1999/xlink" '

KATEX_STYLES = """
<link rel="stylesheet"
    href="https://cdn.jsdelivr.net/npm/katex@0.10.2/dist/katex.css"
    integrity="sha256-SSjvSe9BDSZMUczwnbB1ywCyIk2XaNly9nn6yRm6WJo="
    crossorigin="anonymous">
<style type="text/css">
    .katex img {
      display: block;
      position: absolute;
      width: 100%;
      height: inherit;
    }
</style>
"""


B64IMG_TMPL = '<img src="data:image/svg+xml;base64,{img_text}"/>'


def svg2img(html: str) -> str:
    """Converts inline svg elements to images.

    This is done as a work around for #75 of WeasyPrint
    https://github.com/Kozea/WeasyPrint/issues/75
    """
    while True:
        match = SVG_ELEM_RE.search(html)
        if match:
            svg_text = match.group(0)
            if "xmlns" not in svg_text:
                svg_text = svg_text.replace("<svg ", "<svg " + SVG_XMLNS)
            svg_data = svg_text.encode("utf-8")
            img_b64_data: bytes = base64.standard_b64encode(svg_data)
            img_b64_text = img_b64_data.decode("utf-8")
            img_b64_tag  = B64IMG_TMPL.format(img_text=img_b64_text)
            start, end = match.span()
            html = html[:start] + img_b64_tag + html[end:]
        else:
            break

    return html


def _clean_block_text(block_text: str) -> str:
    if block_text.startswith("```math"):
        block_text = block_text[len("```math") :]
    elif block_text.startswith("~~~math"):
        block_text = block_text[len("~~~math") :]

    if block_text.endswith("```"):
        block_text = block_text[: -len("```")]
    elif block_text.endswith("~~~"):
        block_text = block_text[: -len("~~~")]
    return block_text


def tex2html(tex: str, options: wrapper.Options = None) -> str:
    if options:
        no_inline_svg = options.pop("no_inline_svg", False)
    else:
        no_inline_svg = False

    result = wrapper.tex2html(tex, options)
    if no_inline_svg:
        result = svg2img(result)
    return result


def md_block2html(block_text: str, default_options: wrapper.Options = None) -> str:
    options: wrapper.Options = {'display-mode': True}

    if default_options:
        options.update(default_options)

    block_text = _clean_block_text(block_text)
    header, rest = block_text.split("\n", 1)
    if "{" in header and "}" in header:
        options.update(json.loads(header))
        block_text = rest

    return tex2html(block_text, options)


def _clean_inline_text(inline_text: str) -> str:
    if inline_text.startswith("$``"):
        inline_text = inline_text[len("$``") :]
    if inline_text.startswith("$`"):
        inline_text = inline_text[len("$`") :]
    if inline_text.endswith("``$"):
        inline_text = inline_text[: -len("``$")]
    if inline_text.endswith("`$"):
        inline_text = inline_text[: -len("`$")]
    return inline_text


def md_inline2html(inline_text: str, default_options: wrapper.Options = None) -> str:
    options     = default_options.copy() if default_options else {}
    inline_text = _clean_inline_text(inline_text)
    return tex2html(inline_text, options)


INLINE_DELIM_RE = re.compile(r"`{1,2}")


class InlineCodeItem(typ.NamedTuple):

    inline_text   : str
    marker        : str
    rewritten_line: str


def iter_inline_katex(line: str) -> typ.Iterable[InlineCodeItem]:
    # if line.startswith("4 prelude"):
    #     import pudb; pudb.set_trace()
    pos = 0
    while True:
        inline_match_start = INLINE_DELIM_RE.search(line, pos)
        if inline_match_start is None:
            break

        pos   = inline_match_start.end()
        start = inline_match_start.start()
        delim = inline_match_start.group()

        try:
            end = line.index(delim, start + len(delim)) + (len(delim) - 1)
        except ValueError:
            continue

        pos = end

        if line[start - 1] != "$":
            continue
        if line[end + 1] != "$":
            continue

        inline_text = line[start - 1 : end + 2]
        marker_id   = id(inline_text)
        marker      = f"<span id='katex{marker_id}'>katex{marker_id}</span>"
        line        = line[: start - 1] + marker + line[end + 2 :]

        pos = end + len(delim) - len(inline_text) + len(marker)

        yield InlineCodeItem(inline_text, marker, line)


class KatexExtension(Extension):
    def __init__(self, **kwargs) -> None:
        self.config = {'no_inline_svg': ["", "Replace inline <svg> with <img> tags."]}
        for name, options_text in wrapper.parse_options().items():
            self.config[name] = ["", options_text]

        self.math_html: typ.Dict[str, str] = {}
        super(KatexExtension, self).__init__(**kwargs)

    def reset(self) -> None:
        self.math_html.clear()

    def extendMarkdown(self, md, *args, **kwargs) -> None:
        preproc = KatexPreprocessor(md, self)
        md.preprocessors.register(preproc, name='katex_fenced_code_block', priority=50)

        postproc = KatexPostprocessor(md, self)
        md.postprocessors.register(postproc, name='katex_fenced_code_block', priority=0)
        md.registerExtension(self)


BLOCK_RE = re.compile(r"^(```|~~~)math")


class KatexPreprocessor(Preprocessor):
    def __init__(self, md, ext: KatexExtension) -> None:
        super(KatexPreprocessor, self).__init__(md)
        self.ext: KatexExtension = ext

    def run(self, lines: typ.List[str]) -> typ.List[str]:
        default_options: wrapper.Options = {}
        for name in self.ext.config.keys():
            val = self.ext.getConfig(name, "")
            if val != "":
                default_options[name] = val

        is_in_fence = False
        block_lines: typ.List[str] = []
        out_lines  : typ.List[str] = []

        for line in lines:
            if is_in_fence:
                block_lines.append(line)
                if not ("```" in line or "~~~" in line):
                    continue

                is_in_fence = False
                block_text  = "\n".join(block_lines)
                del block_lines[:]
                math_html = md_block2html(block_text, default_options)
                marker_id = id(block_text)
                marker    = f"<p id='katex{marker_id}'>katex{marker_id}</p>"
                tag_text  = f"<p>{math_html}</p>"
                out_lines.append(marker)
                self.ext.math_html[marker] = tag_text
            elif BLOCK_RE.match(line):
                is_in_fence = True
                block_lines.append(line)
            else:
                for inline_code in iter_inline_katex(line):
                    math_html = md_inline2html(inline_code.inline_text, default_options)
                    self.ext.math_html[inline_code.marker] = math_html
                    line = inline_code.rewritten_line

                out_lines.append(line)

        return out_lines


class KatexPostprocessor(Postprocessor):
    def __init__(self, md, ext: KatexExtension) -> None:
        super(KatexPostprocessor, self).__init__(md)
        self.ext: KatexExtension = ext

    def run(self, text: str) -> str:
        if self.ext.math_html:
            text = KATEX_STYLES + text

        for marker, html in self.ext.math_html.items():
            wrapped_marker = "<p>" + marker + "</p>"
            if wrapped_marker in text:
                text = text.replace(wrapped_marker, html)
            elif marker in text:
                text = text.replace(marker, html)
            else:
                log.warning(f"KatexPostprocessor couldn't find: {marker}")

        return text
