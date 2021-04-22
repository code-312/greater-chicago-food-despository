#!/bin/bash
pytest -p no:warnings tests/test_environment.py
read -p "Press enter to continue..."
python3 src/main.py || python src/main.py