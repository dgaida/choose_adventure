import os
import json
import gradio as gr
from adventure_generator import generate_story

def process_and_save_story(topic, age):
    story_data = generate_story(topic, age)
    if not story_data:
        return "Error: Could not generate story. Please try again."

    # Load template
    template_path = os.path.join(os.path.dirname(__file__), 'templates', 'story_template.html')
    with open(template_path, 'r') as f:
        template_content = f.read()

    # Fill template
    # Replace {{ title }} and {{ story_json }}
    # We use simple string replacement to avoid needing Jinja2 if possible,
    # but the user didn't specify, so let's stick to basics.
    final_html = template_content.replace('{{ title }}', story_data.get('title', 'Adventure Story'))
    final_html = final_html.replace('{{ story_json }}', json.dumps(story_data))

    # Ensure docs directory exists
    docs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'docs')
    os.makedirs(docs_dir, exist_ok=True)

    # Save to docs/index.html
    output_path = os.path.join(docs_dir, 'index.html')
    with open(output_path, 'w') as f:
        f.write(final_html)

    return f"Story generated successfully! Saved to {output_path}. You can now push to GitHub to publish it."

# Create Gradio UI
with gr.Blocks(title="Adventure Story Generator") as demo:
    gr.Markdown("# 📖 Choose Your Own Adventure Story Generator")
    gr.Markdown("Create a branching story tailored for English learners in Germany.")

    with gr.Row():
        topic_input = gr.Textbox(label="Story Topic", placeholder="e.g., A robot in Berlin, A space mission, A haunted castle")
        age_input = gr.Number(label="Age of Pupil", value=12, precision=0)

    generate_btn = gr.Button("Generate and Publish Story")
    output_text = gr.Textbox(label="Status")

    generate_btn.click(
        fn=process_and_save_story,
        inputs=[topic_input, age_input],
        outputs=output_text
    )

if __name__ == "__main__":
    demo.launch()
