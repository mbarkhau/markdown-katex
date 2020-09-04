#!/bin/bash
set -e;

# NOTE (mb 2020-09-04): This is a failed experiment to compress
#   binaries. For our use case this isn't helpful as the python
#   distribution files (.tar.gz and .whl) are already compressed
#   anyway. Even if this gains a few %, the compressed binaries get
#   an additional startup penaulty, which is not worth it.
#
# Results:
#
# 47156856 src/markdown_katex/bin/katex_v0.12.0_x86_64-Darwin
# 49027576 src/markdown_katex/bin/katex_v0.12.0_x86_64-Linux
# 45902222 src/markdown_katex/bin/katex_v0.12.0_x86_64-Windows
#
# 10575888 src/markdown_katex/bin/katex_v0.12.0_x86_64-Darwin-upx
# 12767612 src/markdown_katex/bin/katex_v0.12.0_x86_64-Linux-upx
# 14134670 src/markdown_katex/bin/katex_v0.12.0_x86_64-Windows-upx
#
# 47555241 src/markdown_katex/bin/binfiles.tar.gz
# 34718155 src/markdown_katex/bin/upxfiles.tar.gz


BIN_FILES=$(ls src/markdown_katex/bin/* | awk '! /(-upx|gz)/');

for file in ${BIN_FILES}
do
    if [[ ${file} =~ '-upx' ]]; then
        continue
    fi
    if [[ -f "${file}-upx" ]]; then
        continue
    fi
    upx --brute -o "${file}-upx" ${file};
done

rm -f src/markdown_katex/bin/binfiles.tar.gz
rm -f src/markdown_katex/bin/upxfiles.tar.gz

GZIP=-9 tar -czf src/markdown_katex/bin/binfiles.tar.gz ${BIN_FILES}
GZIP=-9 tar -czf src/markdown_katex/bin/upxfiles.tar.gz src/markdown_katex/bin/*-upx

ls -l src/markdown_katex/bin/* | awk '! /(-upx|gz)$/'
echo ""
ls -l src/markdown_katex/bin/*-upx
echo ""
ls -l src/markdown_katex/bin/*.gz
