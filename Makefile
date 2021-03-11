
PACKAGE_NAME := markdown-katex

# This is the python version that is used for:
# - `make fmt`
# - `make ipy`
# - `make lint`
# - `make devtest`
DEVELOPMENT_PYTHON_VERSION := python=3.9

# These must be valid (space separated) conda package names.
# A separate conda environment will be created for each of these.
#
# Some valid options are:
# - python=2.7
# - python=3.5
# - python=3.6
# - python=3.7
# - pypy2.7
# - pypy3.5
SUPPORTED_PYTHON_VERSIONS := python=3.9 python=2.7 pypy3.5

include Makefile.bootstrapit.make

## -- Extra/Custom/Project Specific Tasks --


TMP_OUTPUT_HTML = $(shell $(DEV_ENV_PY) -c 'import test.test_mdkatex as t;print(t.TMP_DIR / "test_output.html")')
TMP_OUTPUT_PDF = $(shell $(DEV_ENV_PY) -c 'import test.test_mdkatex as t;print(t.TMP_DIR / "test_output.pdf")')


## Render some test html
.PHONY: demo_output
demo_output:
	$(DEV_ENV_PY) -c 'import test.test_mdkatex as t;t.test_html_output()'
	@echo "Wrote to: $(TMP_OUTPUT_HTML)"

	$(DEV_ENV)/bin/weasyprint --quiet $(TMP_OUTPUT_HTML) $(TMP_OUTPUT_PDF)
	@echo "Wrote to: $(TMP_OUTPUT_PDF)"

