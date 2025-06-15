import sys
import os

# This adds the project root to the Python import path.
# We are going up one level from the /tests directory to the /code directory.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))