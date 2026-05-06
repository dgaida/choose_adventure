import os
import json
import logging
import gradio as gr
from typing import Optional
from adventure_generator import generate_story
from update_manifest import update_manifest

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def process_and_save_story(topic: str, level: str, length: str, age_range: str) -> str:
    """
    Orchestrates story generation, saving, and manifest update.

    Args:
        topic: The description of the story to generate.
        level: The CEFR English level.
        length: The length of the story.
        age_range: The age range of the reader.

    Returns:
        A status message indicating success or failure.
    """
    try:
        story_data = generate_story(topic, level, length, age_range)
        if not story_data:
            return "Error: Could not generate story. Please check the logs for details."

        # Ensure docs and docs/stories directories exist
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        docs_dir = os.path.join(base_dir, "docs")
        stories_dir = os.path.join(docs_dir, "stories")
        os.makedirs(stories_dir, exist_ok=True)

        # Generate a filename for the story
        title = story_data.get("title", "story")
        story_id = "".join(x for x in title if x.isalnum())[:20].lower() or "story"
        filename = f"{story_id}_{int(os.getpid())}.json"
        story_path = os.path.join(stories_dir, filename)

        # Save the story JSON
        with open(story_path, "w") as f:
            json.dump(story_data, f, indent=2)

        # Update manifest.json automatically by scanning stories directory
        update_manifest()

        # Ensure index.html is initialized from template
        template_path = os.path.join(os.path.dirname(__file__), "templates", "story_template.html")
        index_path = os.path.join(docs_dir, "index.html")

        if os.path.exists(template_path):
            with open(template_path, "r") as f:
                template_content = f.read()

            with open(index_path, "w") as f:
                f.write(template_content)

        return f"Story '{story_data.get('title')}' generated successfully! Saved to {story_path} and manifest updated. Push to GitHub to publish."
    except Exception as e:
        logger.exception("Error in process_and_save_story")
        return f"An unexpected error occurred: {str(e)}"

# Create Gradio UI
with gr.Blocks(title="Adventure Story Generator") as demo:
    gr.Markdown("# 🗺️ Adventure Story Generator")
    gr.Markdown("Create branching stories for English learners.")

    with gr.Row():
        with gr.Column():
            default_topic = "Create a branching story set in the universe of the 'Warriors' book series by Erin Hunter. It should involve a young apprentice's first hunt and a mysterious prophecy. The story should be appropriate for English learners."
            topic_input = gr.Textbox(label="Story Description", lines=10, value=default_topic)
        with gr.Column():
            level_input = gr.Dropdown(label="English Level", choices=["A1", "A2", "B1", "B2", "C1", "C2"], value="B1")
            length_input = gr.Dropdown(
                label="Story Length",
                choices=["short (15-20 nodes)", "medium (20-25 nodes)", "long (25-30 nodes)"],
                value="short (15-20 nodes)"
            )
            age_input = gr.Dropdown(
                label="Reader Age Range",
                choices=["6-12", "12-18", "18-30", "30-50", "50+"],
                value="12-18"
            )

    generate_btn = gr.Button("Generate and Add to Collection")
    output_text = gr.Textbox(label="Status")

    generate_btn.click(
        fn=process_and_save_story,
        inputs=[topic_input, level_input, length_input, age_input],
        outputs=output_text
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    demo.launch(server_name="0.0.0.0", server_port=port)
