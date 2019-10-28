# This file is part of the markdown-katex project
# https://gitlab.com/mbarkhau/markdown-katex
#
# Copyright (c) 2019 Manuel Barkhau (mbarkhau@gmail.com) - MIT License
# SPDX-License-Identifier: MIT
"""markdown_katex extension.

This is an extension for Python-Markdown which
uses KaTeX to generate html from tex.
"""


__version__ = "v201910.0010-beta"

from markdown_katex.extension import KatexExtension
from markdown_katex.wrapper import tex2html, get_bin_path


def makeExtension(**kwargs) -> KatexExtension:
    return KatexExtension(**kwargs)


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


__all__ = ['makeExtension', '__version__', 'get_bin_path', 'tex2html', 'TEST_FORMULAS']
