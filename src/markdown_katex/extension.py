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
    if inline_text.startswith("$`"):
        inline_text = inline_text[len("$`") :]
    if inline_text.endswith("`$"):
        inline_text = inline_text[: -len("`$")]
    return inline_text


def md_inline2html(inline_text: str, default_options: wrapper.Options = None) -> str:
    options     = default_options.copy() if default_options else {}
    inline_text = _clean_inline_text(inline_text)
    return tex2html(inline_text, options)


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


class KatexPreprocessor(Preprocessor):

    BLOCK_RE  = re.compile(r"^(```|~~~)math")
    INLINE_RE = re.compile(r"\$`.*?`\$")

    def __init__(self, md, ext: KatexExtension) -> None:
        super(KatexPreprocessor, self).__init__(md)
        self.ext: KatexExtension = ext

    def run(self, lines: typ.List[str]) -> typ.List[str]:
        is_in_fence = False
        out_lines  : typ.List[str] = []
        block_lines: typ.List[str] = []

        default_options: wrapper.Options = {}
        for name in self.ext.config.keys():
            val = self.ext.getConfig(name, "")
            if val != "":
                default_options[name] = val

        for line in lines:
            if is_in_fence:
                block_lines.append(line)
                if not ("```" in line or "~~~" in line):
                    continue

                is_in_fence = False
                block_text  = "\n".join(block_lines)
                del block_lines[:]
                math_html    = md_block2html(block_text, default_options)
                math_html_id = id(math_html)
                marker       = f"<p id='katex{math_html_id}'>katex{math_html_id}</p>"
                tag_text     = f"<p>{math_html}</p>"
                out_lines.append(marker)
                self.ext.math_html[marker] = tag_text
            elif self.BLOCK_RE.match(line):
                is_in_fence = True
                block_lines.append(line)
            else:
                while True:
                    inline_match = self.INLINE_RE.search(line)
                    if inline_match is None:
                        break

                    inline_text  = inline_match.group(0)
                    math_html    = md_inline2html(inline_text, default_options)
                    math_html_id = id(math_html)
                    marker       = f"<span id='katex{math_html_id}'>katex{math_html_id}</span>"
                    line         = line.replace(inline_text, marker)
                    self.ext.math_html[marker] = math_html

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
