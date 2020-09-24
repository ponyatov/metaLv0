#!/bin/sh
sed -ri "s/[A-Za-z\.]+\.py/$1.py/g;" .vscode/launch.json
sed -ri "s/[A-Za-z\.]+\/repl/$1\/repl/g;" .vscode/settings.json
code $1.py
