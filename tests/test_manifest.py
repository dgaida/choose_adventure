import os
import json
import pytest
from update_manifest import update_manifest

def test_manifest_integration():
    # Ensure we are in the repo root
    base_dir = os.getcwd()
    stories_dir = os.path.join(base_dir, 'docs', 'stories')
    test_story_path = os.path.join(stories_dir, 'test_temp_story.json')
    manifest_path = os.path.join(stories_dir, 'manifest.json')

    # Backup original manifest if exists
    backup_manifest = None
    if os.path.exists(manifest_path):
        with open(manifest_path, 'r') as f:
            backup_manifest = f.read()

    try:
        # Create stories directory if it doesn't exist
        os.makedirs(stories_dir, exist_ok=True)

        # Create a temp story
        with open(test_story_path, 'w') as f:
            json.dump({"title": "Test Temp Story", "nodes": {}}, f)

        update_manifest()

        assert os.path.exists(manifest_path), f"Manifest file {manifest_path} was not created"

        with open(manifest_path, 'r') as f:
            manifest = json.load(f)

        titles = [s['title'] for s in manifest['stories']]
        assert "Test Temp Story" in titles

    finally:
        if os.path.exists(test_story_path):
            os.remove(test_story_path)
        update_manifest() # Restore manifest content
        if backup_manifest:
            with open(manifest_path, 'w') as f:
                f.write(backup_manifest)
