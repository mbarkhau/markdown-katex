FROM registry.gitlab.com/mbarkhau/markdown-katex/base

ADD src/ src/
ADD stubs/ stubs/
ADD test/ test/
ADD requirements/ requirements/
ADD setup.cfg setup.cfg
ADD setup.py setup.py
ADD README.md README.md
ADD CHANGELOG.md CHANGELOG.md
ADD LICENSE LICENSE
ADD makefile makefile
ADD makefile.bootstrapit.make makefile.bootstrapit.make

ENV PYTHONPATH="src/:vendor/"

CMD make lint test
