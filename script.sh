#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

echo -e "${CYAN}${BOLD}Hello Ninja!${NC}"
echo -e "${BLUE}Welcome to the voting dojo${NC}"
echo -e "${MAGENTA}-------------------------------------------------------------------------${NC}"

echo -e -n "${YELLOW}Please enter your name: ${NC}"
read name

echo -e -n "${YELLOW}Enter your age: ${NC}"
read age

echo -e "${MAGENTA}-------------------------------------------------------------------------${NC}"

# Check if age is a valid number
if ! [[ "$age" =~ ^[0-9]+$ ]]; then
    echo -e "${RED}${BOLD}Error: Please enter a valid number for your age!${NC}"
    exit 1
fi

if [ "$age" -ge 18 ]; then
    echo -e "${GREEN}${BOLD}Awesome $name! You are $age years old and eligible to vote in the dojo! 🗳️${NC}"
else
    years_left=$((18 - age))
    echo -e "${RED}Sorry $name, you are only $age. You need to wait $years_left more year(s) to vote. 🥋${NC}"
fi
