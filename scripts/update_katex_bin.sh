#!/bin/bash
set -e;

PROJECT_DIR=$PWD
cd ../KaTeX

git checkout .
git checkout main
git pull

TAG=$(git tag -l --sort=taggerdate | grep -E "^v[0-9]+\.[0-9]+.[0-9]+$" | sort --version-sort | tail -n 1)
echo $TAG
git checkout $TAG

rm -f cli-linux
rm -f cli-macos
rm -f cli-win.exe

npm install -g pkg
npm install -g yarn

yarn
yarn build

npm install commander

# node10 produces smaller binaries but doesn't work for windows
pkg --target node12-win-x64,node10-linux-x64,node10-macos-x64 cli.js

BIN=${PROJECT_DIR}/src/markdown_katex/bin
mkdir -p $BIN

wine cli-node12-win.exe --version
./cli-node10-linux --version
# darling cli-node10-macos --version

mv cli-node12-win.exe $BIN/katex_${TAG}_node12_x86_64-Windows.exe
mv cli-node10-linux $BIN/katex_${TAG}_node10_x86_64-Linux
mv cli-node10-macos $BIN/katex_${TAG}_node10_x86_64-Darwin

ls -l $BIN/*
file $BIN/*

echo "all ok"
