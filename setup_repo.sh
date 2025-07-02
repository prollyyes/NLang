#!/usr/bin/env bash
set -euo pipefail

# List of directories to create
dirs=(
  "grammar"
  "src/lexer"
  "src/parser"
  "examples"
  "tests"
  "docs"
  ".github/workflows"
  "scripts"
)

echo "Creating directory structure…"
for d in "${dirs[@]}"; do
  mkdir -p "$d"
done

# List of placeholder files to touch
files=(
  "grammar/aion.ebnf"
  "LICENSE"
  ".gitignore"
  ".github/workflows/ci.yml"
  "scripts/build.sh"
)

echo "Creating placeholder files…"
for f in "${files[@]}"; do
  if [ ! -e "$f" ]; then
    touch "$f"
  fi
done

echo "All done! 🌱"
