#!/usr/bin/env bash
# ============================================================
#  Zelex Collector's Gallery - macOS / Linux launcher
#
#  Starts a small local web server (best quality) using Python 3,
#  which comes preinstalled on macOS and most Linux systems.
#  If Python isn't available it opens the page directly.
#
#  macOS: double-click this file (you may need to right-click >
#         Open the first time to bypass Gatekeeper).
#  Linux: run  ./Start-Mac-Linux.command  in a terminal.
# ============================================================

# Move to the folder this script lives in.
cd "$(dirname "$0")" || exit 1

open_file() {
  # Open index.html in the default browser, OS-dependent.
  if command -v open >/dev/null 2>&1; then
    open "index.html"          # macOS
  elif command -v xdg-open >/dev/null 2>&1; then
    xdg-open "index.html"      # Linux
  else
    echo "Please open index.html in your browser manually."
  fi
}

if command -v python3 >/dev/null 2>&1; then
  echo "Starting local server with Python 3..."
  python3 serve.py
elif command -v python >/dev/null 2>&1; then
  echo "Starting local server with Python..."
  python serve.py
else
  echo "Python not found - opening the page directly instead."
  open_file
fi
