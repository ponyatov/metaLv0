#!/bin/sh
sed -ri "s/[a-z]+\.py/$1.py/g;" .vscode/launch.json
sed -ri "s/[a-z]+\/repl/$1\/repl/g;" .vscode/settings.json
code $1.py
