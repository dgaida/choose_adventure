import os
from adventure_generator import generate_story
from app import process_and_save_story

# adventure_generator.py changes
# - Added length and age_range parameters
# - Set default model to "openai/gpt-oss-120b"
# - Increased max_tokens to 4096

# app.py changes
# - Added Story Length and Reader Age Range dropdowns
# - Updated process_and_save_story to handle new inputs
