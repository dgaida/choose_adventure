import os
import json
import logging

logger = logging.getLogger(__name__)


def update_manifest():
    """
    Scans the docs/stories directory and updates manifest.json
    with the list of available stories.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    stories_dir = os.path.join(base_dir, "docs", "stories")
    manifest_path = os.path.join(stories_dir, "manifest.json")

    if not os.path.exists(stories_dir):
        logger.warning(f"Stories directory not found: {stories_dir}")
        return

    stories = []
    for filename in os.listdir(stories_dir):
        if filename.endswith(".json") and filename != "manifest.json":
            file_path = os.path.join(stories_dir, filename)
            try:
                with open(file_path, "r") as f:
                    data = json.load(f)
                    stories.append({
                        "title": data.get("title", "Untitled Story"),
                        "filename": filename
                    })
            except Exception as e:
                logger.error(f"Error reading {filename}: {e}")

    # Sort stories by title
    stories.sort(key=lambda x: x["title"])

    manifest_data = {"stories": stories}

    with open(manifest_path, "w") as f:
        json.dump(manifest_data, f, indent=2)

    logger.info(f"Manifest updated with {len(stories)} stories.")


if __name__ == "__main__":
    update_manifest()
