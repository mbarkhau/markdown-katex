# This file is part of the markdown-katex project
# https://gitlab.com/mbarkhau/markdown-katex
#
# Copyright (c) 2019 Manuel Barkhau (mbarkhau@gmail.com) - MIT License
# SPDX-License-Identifier: MIT

# NOTE (mb 2019-05-16): This module is substantially shared with the
#   markdown-katex package and meaningful changes should be
#   replicated there also.

import os
import re
import time
import signal
import hashlib
import tempfile
import platform
import typing as typ
import pathlib2 as pl
import subprocess as sp


SIG_NAME_BY_NUM = {
    k: v
    for v, k in reversed(sorted(signal.__dict__.items()))
    if v.startswith('SIG') and not v.startswith('SIG_')
}

assert SIG_NAME_BY_NUM[15] == 'SIGTERM'


TMP_DIR = pl.Path(tempfile.gettempdir()) / "mdkatex"

LIBDIR: pl.Path = pl.Path(__file__).parent
PKG_BIN_DIR      = LIBDIR / "bin"
FALLBACK_BIN_DIR = pl.Path("/") / "usr" / "local" / "bin"
FALLBACK_BIN_DIR = FALLBACK_BIN_DIR.expanduser()

CMD_NAME = "katex"


def _get_usr_bin_path() -> typ.Optional[pl.Path]:
    env_path = os.environ.get('PATH')
    env_paths: typ.List[pl.Path] = []

    if env_path:
        path_strs = env_path.split(os.pathsep)
        env_paths.extend([pl.Path(p) for p in path_strs])

    # search in fallback bin dir regardless of path
    if FALLBACK_BIN_DIR not in env_paths:
        env_paths.append(FALLBACK_BIN_DIR)

    for path in env_paths:
        local_bin = path / CMD_NAME
        if local_bin.exists():
            return local_bin

        local_bin = path / f"{CMD_NAME}.exe"
        if local_bin.exists():
            return local_bin

    return None


# https://pymotw.com/3/platform/
OSNAME  = platform.system()
MACHINE = platform.machine()


def _get_pkg_bin_path(osname: str = OSNAME, machine: str = MACHINE) -> pl.Path:
    if machine == 'AMD64':
        machine = 'x86_64'
    glob_expr = f"*_{machine}-{osname}"
    bin_files = list(PKG_BIN_DIR.glob(glob_expr))
    if bin_files:
        return max(bin_files)

    err_msg = (
        "Platform not supported, "
        "katex binary not found. "
        "Install manually using "
        "'npm install katex'."
    )

    raise NotImplementedError(err_msg)


def get_bin_path() -> pl.Path:
    usr_bin_path = _get_usr_bin_path()
    if usr_bin_path:
        return usr_bin_path
    else:
        return _get_pkg_bin_path()


def _iter_output_lines(buf: typ.IO[bytes]) -> typ.Iterable[bytes]:
    while True:
        output = buf.readline()
        if output:
            yield output
        else:
            return


def read_output(buf: typ.IO[bytes]) -> str:
    return b"".join(_iter_output_lines(buf)).decode("utf-8")


ArgValue = typ.Union[str, int, float, bool]
Options  = typ.Dict[str, ArgValue]


def tex2html(tex: str, options: Options = None) -> str:
    binpath   = get_bin_path()
    cmd_parts = [str(binpath)]

    if options:
        for option_name, option_value in options.items():
            if option_name.startswith("--"):
                arg_name = option_name
            else:
                arg_name = "--" + option_name

            if option_value is True:
                cmd_parts.append(arg_name)
            elif option_value is False:
                continue
            else:
                arg_value = str(option_value)
                cmd_parts.append(arg_name)
                cmd_parts.append(arg_value)

    input_data = tex.encode("utf-8")

    hasher = hashlib.sha256(input_data)
    for cmd_part in cmd_parts:
        hasher.update(cmd_part.encode("utf-8"))

    digest = hasher.hexdigest()

    tmp_input_file  = TMP_DIR / (digest + ".tex")
    tmp_output_file = TMP_DIR / (digest + ".html")

    if tmp_output_file.exists():
        tmp_output_file.touch()
    else:
        cmd_parts.extend(["--input", str(tmp_input_file), "--output", str(tmp_output_file)])

        TMP_DIR.mkdir(parents=True, exist_ok=True)
        with tmp_input_file.open(mode="wb") as fobj:
            fobj.write(input_data)

        proc     = sp.Popen(cmd_parts, stdout=sp.PIPE, stderr=sp.PIPE)
        ret_code = proc.wait()
        if ret_code < 0:
            signame = SIG_NAME_BY_NUM[abs(ret_code)]
            err_msg = (
                f"Error processing '{tex}': "
                + "katex_cli process ended with "
                + f"code {ret_code} ({signame})"
            )
            raise Exception(err_msg)
        elif ret_code > 0:
            stdout  = read_output(proc.stdout)
            errout  = read_output(proc.stderr)
            output  = (stdout + "\n" + errout).strip()
            err_msg = f"Error processing '{tex}': {output}"
            raise Exception(err_msg)

        tmp_input_file.unlink()

    with tmp_output_file.open(mode="r") as fobj:
        result = fobj.read()

    _cleanup_tmp_dir()

    return result


def _cleanup_tmp_dir() -> None:
    min_mtime = time.time() - 24 * 60 * 60
    for fpath in TMP_DIR.iterdir():
        if not fpath.is_file():
            continue
        mtime = fpath.stat().st_mtime
        if mtime < min_mtime:
            fpath.unlink()


# NOTE: in order to not have to update the code
#   of the extension any time an option is added,
#   we parse the help text of the katex command.


DEFAULT_HELP_TEXT = r"""
Options:
  -V, --version              output the version number
  -d, --display-mode         Render math in display...
  --leqno                    Render display math in...
  --fleqn                    Render display math fl...
  -t, --no-throw-on-error    Render errors (in the ...
  -c, --error-color <color>  A color string given i...
  -b, --color-is-text-color  Makes \color behave li...
  -S, --strict               Turn on strict / LaTeX...
  -s, --max-size <n>         If non-zero, all user-...
  -e, --max-expand <n>       Limit the number of ma...
  -m, --macro <def>          Define custom macro of...
  -f, --macro-file <path>    Read macro definitions...
  -i, --input <path>         Read LaTeX input from ...
  -o, --output <path>        Write html output to t...
  -h, --help                 output usage information
"""

DEFAULT_HELP_TEXT = DEFAULT_HELP_TEXT.replace("\n", " ").replace("NL", "\n")


def _get_cmd_help_text() -> str:
    binpath   = get_bin_path()
    cmd_parts = [str(binpath), "--help"]
    proc      = sp.Popen(cmd_parts, stdout=sp.PIPE)
    help_text = read_output(proc.stdout)
    return help_text


OptionsHelp = typ.Dict[str, str]

# https://regex101.com/r/287NYS/4
OPTION_PATTERN = r"""
    --
    (?P<name>[a-z\-]+)
    \s+(?:<[a-z\-]+>)?
    \s+
    (?P<text>[^\n]*[ \s\w(){},:;.'\\/\[\] ]*)
"""
OPTION_REGEX = re.compile(OPTION_PATTERN, flags=re.VERBOSE | re.DOTALL | re.MULTILINE)


def _parse_options_help_text(help_text: str) -> OptionsHelp:
    options: OptionsHelp = {}

    options_text = help_text.split("Options:", 1)[-1]

    for match in OPTION_REGEX.finditer(options_text):
        name = match.group("name")
        text = match.group("text")
        text = " ".join(l.strip() for l in text.splitlines())
        options[name] = text.strip()

    options.pop("version"     , None)
    options.pop("help"        , None)
    options.pop("input"       , None)
    options.pop("output"      , None)
    options.pop("display-mode", None)
    options.pop("macro-file"  , None)

    return options


_PARSED_OPTIONS: OptionsHelp = {}


def parse_options() -> OptionsHelp:
    if _PARSED_OPTIONS:
        return _PARSED_OPTIONS

    options = _parse_options_help_text(DEFAULT_HELP_TEXT)
    try:
        help_text   = _get_cmd_help_text()
        cmd_options = _parse_options_help_text(help_text)
        options.update(cmd_options)
    except NotImplementedError:
        # NOTE: no need to fail just for the options
        pass

    _PARSED_OPTIONS.update(options)
    return options
