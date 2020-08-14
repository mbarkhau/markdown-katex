# This file is part of the markdown-katex project
# https://gitlab.com/mbarkhau/markdown-katex
#
# Copyright (c) 2020 Manuel Barkhau (mbarkhau@gmail.com) - MIT License
# SPDX-License-Identifier: MIT
_STYLESHEET_LINK = """
<link rel="stylesheet"
    href="https://cdn.jsdelivr.net/npm/katex@0.12.0/dist/katex.min.css"
    integrity="sha384-AfEj0r4/OFrOo5t7NnNe46zW/tFgW6x/bCJG8FqQCEo3+Aro6EYUG4+cU+KJWu/X"
    crossorigin="anonymous" />
"""

_KATEX_IMAGE_STYLES = """
<style type="text/css">
    .katex img {
      display: block;
      position: absolute;
      width: 100%;
      height: inherit;
    }
</style>
"""

KATEX_STYLES = _STYLESHEET_LINK + _KATEX_IMAGE_STYLES


HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
  <title>Test Katex</title>
  {{stylesheet_link}}
  <style type="text/css">
    body{background: white; }
  </style>
</head>
<body>
Generated with markdown-katex
<hr/>
{{content}}
</body>
</html>
"""

HTML_TEMPLATE = HTML_TEMPLATE.replace("{{stylesheet_link}}", _STYLESHEET_LINK)
