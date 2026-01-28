#!/usr/bin/env bash
set -euo pipefail

if command -v apt-get >/dev/null 2>&1; then
  sudo apt-get update
  sudo apt-get install -y graphviz
elif command -v yum >/dev/null 2>&1; then
  sudo yum install -y graphviz
elif command -v dnf >/dev/null 2>&1; then
  sudo dnf install -y graphviz
elif command -v pacman >/dev/null 2>&1; then
  sudo pacman -S --noconfirm graphviz
elif command -v brew >/dev/null 2>&1; then
  brew install graphviz
else
  echo "No supported package manager found. Please install Graphviz manually." >&2
  exit 1
fi
