#!/bin/bash

# Define colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${CYAN}======================================${NC}"
echo -e "${CYAN}     VoxCore Mac Setup Script         ${NC}"
echo -e "${CYAN}======================================${NC}\n"

# 1. Check for Homebrew
echo -e "${YELLOW}[1/3] Checking for Homebrew...${NC}"
if ! command -v brew &> /dev/null; then
    echo -e "${RED}Error: Homebrew is not installed.${NC}"
    echo "Please install it by running:"
    echo '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
    exit 1
else
    echo -e "${GREEN}Homebrew found!${NC}"
fi

# 2. Install Mac Audio Headers
echo -e "\n${YELLOW}[2/3] Installing PortAudio hardware headers...${NC}"
brew install portaudio

# 3. Install Python Dependencies with the Mac Compiler Fix
echo -e "\n${YELLOW}[3/3] Installing Python AI and Audio libraries...${NC}"
# This injects the exact Homebrew paths into pip so pyaudio doesn't crash
LDFLAGS="-L$(brew --prefix portaudio)/lib" CPPFLAGS="-I$(brew --prefix portaudio)/include" pip3 install pyaudio SpeechRecognition openai-whisper soundfile

# Finish
echo -e "\n${GREEN}======================================${NC}"
echo -e "${GREEN} Setup Complete! You can now run:${NC}"
echo -e "${GREEN} python3 main.py${NC}"
echo -e "${GREEN}======================================${NC}\n"