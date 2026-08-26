#!/usr/bin/env bash
# Build inside a container, because WeasyPrint needs GTK and Windows has none.
#
# MSYS_NO_PATHCONV stops Git Bash rewriting the container-side paths into
# Windows ones, which is the failure that looks like "no such file" for a file
# that is plainly there.
set -euo pipefail

MSYS_NO_PATHCONV=1 docker run --rm \
  -v "$(pwd):/app" -w /app \
  python:3.12-slim \
  sh -c "apt-get update -qq && \
         apt-get install -y -qq --no-install-recommends \
           libpango-1.0-0 libpangoft2-1.0-0 libcairo2 libgdk-pixbuf-2.0-0 \
           libffi-dev shared-mime-info fonts-dejavu fonts-liberation \
           >/dev/null && \
         pip install --quiet -r requirements.txt && \
         python build.py $*"
