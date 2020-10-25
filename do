#!/bin/sh
sed -ri "s/[A-Za-z0-9\.\-]+\.py/$1.py/g;" .vscode/launch.json
sed -ri "s/[A-Za-z0-9\.\-]+\/repl/$1\/repl/g;" .vscode/settings.json
code $1.py
