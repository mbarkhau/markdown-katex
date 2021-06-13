# This file is part of the markdown-katex project
# https://github.com/mbarkhau/markdown-katex
#
# Copyright (c) 2019-2021 Manuel Barkhau (mbarkhau@gmail.com) - MIT License
# SPDX-License-Identifier: MIT
"""markdown_katex extension.

This is an extension for Python-Markdown which
uses KaTeX to generate html from tex.
"""


__version__ = "v202106.1032"

from markdown_katex.wrapper import tex2html
from markdown_katex.wrapper import get_bin_cmd
from markdown_katex.extension import KatexExtension


def _make_extension(**kwargs) -> KatexExtension:
    return KatexExtension(**kwargs)


# Name that conforms with the Markdown extension API
# https://python-markdown.github.io/extensions/api/#dot_notation
makeExtension = _make_extension


TEST_FORMULAS = r"""
f(x) = \int_{-\infty}^\infty
\hat f(\xi)\,e^{2 \pi i \xi x}
\,d\xi

---

\displaystyle

\frac{1}{
  \Bigl(\sqrt{\phi \sqrt{5}}-\phi\Bigr) e^{\frac25 \pi}
} =
 1+\frac{e^{-2\pi}} {
   1+\frac{e^{-4\pi}} {
     1+\frac{e^{-6\pi}} {
       1+\frac{e^{-8\pi}}{
         1+\cdots
       }
     }
   }
}

---

\displaystyle

\left
  ( \sum_{k=1}^n a_k b_k
\right)^2

\leq

\left(
  \sum_{k=1}^n a_k^2
\right)
\left(
  \sum_{k=1}^n b_k^2
\right)

---

\overbrace{x + \cdots + x}^{n\rm\ times}
-
\underbrace{x + \cdots + x}_{n\rm\ times}

---

\oiiint \oiint \oint  \frac ab + {\scriptscriptstyle \frac cd + \frac ef} + \frac gh

---

\Overrightarrow{ABCDE}
-
\overrightharpoon{abcdec}
-
\overgroup{ABCDEF}
-
\undergroup{abcde}
-
\undergroup{efgp}
-
\utilde{AB}
-
\utilde{\utilde{\utilde{AB}}}
-
\widecheck{AB\widecheck{CD}EF}
-
\widehat{AB\widehat{CD}EF}

""".split(
    "---"
)


__all__ = ['makeExtension', '__version__', 'get_bin_cmd', 'tex2html', 'TEST_FORMULAS']
