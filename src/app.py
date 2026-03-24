import os
import json
import gradio as gr
from adventure_generator import generate_story
from update_manifest import update_manifest

def process_and_save_story(topic, age):
    story_data = generate_story(topic, age)
    if not story_data:
        return "Error: Could not generate story. Please try again."

    # Ensure docs and docs/stories directories exist
    base_dir = os.path.dirname(os.path.dirname(__file__))
    docs_dir = os.path.join(base_dir, 'docs')
    stories_dir = os.path.join(docs_dir, 'stories')
    os.makedirs(stories_dir, exist_ok=True)

    # Generate a filename for the story
    story_id = "".join(x for x in topic if x.isalnum())[:20].lower() or "story"
    filename = f"{story_id}_{int(os.getpid())}.json"
    story_path = os.path.join(stories_dir, filename)

    # Save the story JSON
    with open(story_path, 'w') as f:
        json.dump(story_data, f, indent=2)

    # Update manifest.json automatically by scanning stories directory
    update_manifest()

    # Ensure index.html is initialized from template
    template_path = os.path.join(os.path.dirname(__file__), 'templates', 'story_template.html')
    index_path = os.path.join(docs_dir, 'index.html')

    with open(template_path, 'r') as f:
        template_content = f.read()

    # For the multi-story version, the template doesn't need replacements
    # as it loads data via JS. Just copy it.
    with open(index_path, 'w') as f:
        f.write(template_content)

    return f"Story '{story_data.get('title')}' generated successfully! Saved to {story_path} and manifest updated. Push to GitHub to publish."

# Create Gradio UI
with gr.Blocks(title="Warriors Adventure Generator") as demo:
    gr.Markdown("# 🐈 Warriors: Choose Your Own Adventure Generator")
    gr.Markdown("Create branching stories set in the Warriors universe for English learners.")

    with gr.Row():
        topic_input = gr.Textbox(label="Story Topic", placeholder="e.g., An apprentice's first hunt, A battle between Clans, A secret prophecy")
        age_input = gr.Number(label="Age of Pupil", value=12, precision=0)

    generate_btn = gr.Button("Generate and Add to Collection")
    output_text = gr.Textbox(label="Status")

    generate_btn.click(
        fn=process_and_save_story,
        inputs=[topic_input, age_input],
        outputs=output_text
    )

if __name__ == "__main__":
    demo.launch()
