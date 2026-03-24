import os
import json

def update_manifest():
    # Use absolute path to find stories directory relative to this script
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    stories_dir = os.path.join(base_dir, 'docs', 'stories')
    manifest_path = os.path.join(stories_dir, 'manifest.json')

    stories = []
    if os.path.exists(stories_dir):
        # Sort filenames to ensure consistent manifest order
        for filename in sorted(os.listdir(stories_dir)):
            if filename.endswith('.json') and filename != 'manifest.json':
                filepath = os.path.join(stories_dir, filename)
                try:
                    with open(filepath, 'r') as f:
                        story_data = json.load(f)
                        stories.append({
                            "title": story_data.get('title', filename),
                            "filename": filename
                        })
                except Exception as e:
                    print(f"Error reading {filename}: {e}")

    manifest = {"stories": stories}

    # Ensure the directory exists
    os.makedirs(stories_dir, exist_ok=True)
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)
    print(f"Updated {manifest_path} with {len(stories)} stories.")

if __name__ == "__main__":
    update_manifest()
