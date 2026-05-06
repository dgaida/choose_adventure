import os
import sys
# Set up paths
sys.path.append(os.path.join(os.getcwd(), 'src'))

try:
    from app import process_and_save_story
    from adventure_generator import generate_story
    print("Imports successful")
except Exception as e:
    print(f"Import failed: {e}")
    sys.exit(1)
