# Changelog for https://gitlab.com/mbarkhau/markdown-katex

## Contributors

Thank you to for testing, reporting issues and contributing patches:

- @summersz - Richard Summers
- @bluhme3 - Evan Bluhm
- @pawamoy - Timothée Mazzucotelli
- @briankchan
- @spoorendonk
- @lisongmin
- @alexatadi
- @sacredfox - Akihiro Nomura


## v202103.1029

 - Fix [#14](https://gitlab.com/mbarkhau/markdown-katex/-/issues/14): Since `Markdown>=3.3` support for [Markdown in HTML][md_in_html] was broken.

[md_in_html]: https://python-markdown.github.io/extensions/md_in_html/

Thank you @summersz for reporting this issue.


## v202103.1028

 - Use node12 for KaTeX binary on Windows


## v202103.1027

 - Update KaTeX binaries to v0.13.0


## v202008.1026

 - Fix [#12](https://gitlab.com/mbarkhau/markdown-katex/-/issues/12): Bug in handling of paths with whitespace. (Thanks @summersz !)


## v202008.1025

 - Fix [#9](https://gitlab.com/mbarkhau/markdown-katex/-/issues/9): Update `katex.css`
 - Fix [#8](https://gitlab.com/mbarkhau/markdown-katex/-/issues/8): Lookup of binaries on windows
 - Update documentation wrt. use with WeasyPrint


## v202008.1024

 - Update KaTeX binaries to v0.12.0
 - Fix [#8](https://gitlab.com/mbarkhau/markdown-katex/-/issues/8): Update binaries...
 - Fix [#7](https://gitlab.com/mbarkhau/markdown-katex/-/issues/7): Lookup of binaries via npx


## v202006.1021

 - Fix [#7](https://gitlab.com/mbarkhau/markdown-katex/-/issues/7): File encoding issue on Windows.


## v202006.1020

 - Fix [#7](https://gitlab.com/mbarkhau/markdown-katex/-/issues/7) katex-cli on Windows (now uses pkg --target node12...)
 - Fix search for local `katex.ps1`, `katex.cmd`, `katex.exe` on Windows.


## v202005.0017

 - Allow use of `macro-file` option.
 - Update katex-cli to [version v0.11.1](https://github.com/KaTeX/KaTeX/blob/master/CHANGELOG.md)


## v202005.0016-beta

 - Fix #6: [Regression in code block parsing](https://gitlab.com/mbarkhau/markdown-katex/-/issues/6), introduced in `v202004.0015-beta`


## v202004.0015-beta

 - Fix #3: [Inline math inside block](https://gitlab.com/mbarkhau/markdown-katex/-/issues/3)


## v202004.0014-beta

 - Fix #4: [Link tag not properly closed](https://gitlab.com/mbarkhau/markdown-katex/-/issues/4)


## v202001.0013-beta

 - Fix: Ignore trailing whitespace after closing fence.


## v202001.0012-beta

 - Fix: Remove extraneous whitespace to work better with whitespace: pre.


## v201912.0011-beta

 - Add option `insert_fonts_css`
 - Document options


## v201910.0010-beta

 - Add more prominent example to README.md
 - Fix #2: Fix spurious log message when using MkDocs


## v201908.0009-beta

 - Fix #1: Wrong formulas are rendered when multiple formulas are in one doc.


## v201907.0008-beta

 - Fix: don't require typing package for py<35


## v201905.0007-beta

 - Fix: Parsing of inline code when using multiple backticks


## v201905.0004-beta

 - Fix: better error reporting
 - Fix: cleanup temp dir


## v201905.0002-alpha

 - Initial release
