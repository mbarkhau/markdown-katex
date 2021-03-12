#!/usr/bin/env python
# This file is part of the markdown-katex project
# https://github.com/mbarkhau/markdown-katex
#
# Copyright (c) 2019-2021 Manuel Barkhau (mbarkhau@gmail.com) - MIT License
# SPDX-License-Identifier: MIT
import sys
import json
import typing as typ
import subprocess as sp

import markdown_katex
from markdown_katex import html

try:
    import pretty_traceback

    pretty_traceback.install()
except ImportError:
    pass  # no need to fail because of missing dev dependency


ExitCode = int


def _selftest() -> ExitCode:
    # pylint:disable=import-outside-toplevel  ; lazy import to improve cli responsiveness
    from markdown_katex import wrapper

    print("Command options:")
    print(json.dumps(wrapper.parse_options(), indent=4))
    print()

    html_parts: typ.List[str] = []
    test_formulas = markdown_katex.TEST_FORMULAS

    for tex_formula in test_formulas:
        html_part = wrapper.tex2html(tex_formula)
        if not html_part:
            return 1

        html_parts.append(html_part)

    formula_html = "\n<hr/>\n".join(html_parts)
    html_text    = html.HTML_TEMPLATE.replace("{{content}}", formula_html)

    with open("test.html", mode="wb") as fobj:
        fobj.write(html_text.encode("utf-8"))

    print("Created 'test.html'")
    return 0


def main(args: typ.Sequence[str] = sys.argv[1:]) -> ExitCode:
    """Basic wrapper around the katex command.

    This is mostly just used for self testing.
    $ python -m markdown_katex
    """
    # pylint:disable=dangerous-default-value ; mypy will catch mutations of args

    if "--markdown-katex-selftest" in args:
        return _selftest()

    bin_cmd = markdown_katex.get_bin_cmd()

    if "--version" in args or "-V" in args:
        version = markdown_katex.__version__
        bin_str = " ".join(bin_cmd)
        print("markdown-katex version: ", version, f"(using binary: {bin_str})")

    return sp.check_call(bin_cmd + list(args))


if __name__ == '__main__':
    sys.exit(main())
