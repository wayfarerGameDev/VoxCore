#!/bin/bash

# 1. Force the script to run from its own directory
cd "$(dirname "$0")" || exit 1

BUILD_NAME="${1:-vox_core}"
if [ -f "./Build/$BUILD_NAME" ]; then
   ./Build/"$BUILD_NAME"
   exit 0
fi
exit 1