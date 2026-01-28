#!/bin/bash
# NYC Plow Navigator - Quick Start Script
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python plow_navigator.py
