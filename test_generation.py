import json
import os
import sys

# Mocking the LLM response
mock_story = {
    "title": "A Mysterious Forest Adventure",
    "nodes": {
        "start": {
            "text": "You stand at the edge of a mysterious forest. The trees are tall and dark. You see a path going left and a path going right.",
            "choices": [
                { "text": "Go left", "next_node": "left_path" },
                { "text": "Go right", "next_node": "right_path" }
            ]
        },
        "left_path": {
            "text": "The left path is narrow. You find a shiny key on the ground.",
            "choices": []
        },
        "right_path": {
            "text": "The right path is wide. You see a friendly deer.",
            "choices": []
        }
    },
    "vocabulary": {
        "mysterious": "strange and unknown",
        "edge": "the part where something begins or ends",
        "narrow": "not wide"
    }
}

# We need to mock generate_story BEFORE it is imported by src.app
# Actually src.app imports it from adventure_generator
import types
ag_mock = types.ModuleType('adventure_generator')
ag_mock.generate_story = lambda topic, age: mock_story
sys.modules['adventure_generator'] = ag_mock

from src.app import process_and_save_story

result = process_and_save_story("Test Topic", 12)
print(result)

if os.path.exists("docs/index.html"):
    print("docs/index.html created successfully.")
    with open("docs/index.html", "r") as f:
        content = f.read()
        if 'A Mysterious Forest Adventure' in content and 'mysterious' in content:
            print("HTML content looks correct.")
        else:
            print("HTML content might be missing some parts.")
else:
    print("docs/index.html was NOT created.")
