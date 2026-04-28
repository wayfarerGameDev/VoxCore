#!/bin/bash

echo "========================================"
echo "  Starting Mac Dependency Installer...  "
echo "========================================"

# Step 1: Ensure Homebrew is ready
echo "-> Updating Homebrew..."
brew update

# Step 2: Install core Mac system libraries
# - mpv: Required for your background radio
# - ffmpeg: Required for OpenAI Whisper to process audio
# - libsndfile: Required for SpeechRecognition's soundfile backend
echo "-> Installing system libraries via Homebrew..."
brew install mpv ffmpeg libsndfile

# Step 3: Install Python packages
# Using pip3 and overriding the managed environment warning
echo "-> Installing Python packages via pip3..."
pip3 install rapidfuzz pynput python-mpv SpeechRecognition openai-whisper soundfile --break-system-packages

echo "========================================"
echo "  Installation Complete! Everything is  "
echo "  ready for your duck-typed services.   "
echo "========================================"