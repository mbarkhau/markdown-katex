#!/usr/bin/env python
# This file is part of the markdown-katex project
# https://gitlab.com/mbarkhau/markdown-katex
#
# Copyright (c) 2019 Manuel Barkhau (mbarkhau@gmail.com) - MIT License
# SPDX-License-Identifier: MIT
import os
import click
import markdown_katex


# To enable pretty tracebacks:
#   echo "export ENABLE_BACKTRACE=1;" >> ~/.bashrc
if os.environ.get('ENABLE_BACKTRACE') == "1":
    import backtrace
    backtrace.hook(align=True, strip_path=True, enable_on_envvar_only=True)


click.disable_unicode_literals_warning = True


@click.group()
def cli() -> None:
    """markdown_katex cli."""


@cli.command()
@click.version_option(version="v201905.0001-alpha")
def version() -> None:
    """Show version number."""
    print(f"markdown_katex version: {markdown_katex.__version__}")
