# Adventure Story Generator

[![Auto Versioning & Badges](https://github.com/dgaida/adventure-story-generator/actions/workflows/versioning-and-badges.yml/badge.svg)](https://github.com/dgaida/adventure-story-generator/actions/workflows/versioning-and-badges.yml)

A "choose your own adventure" story generator for English learners in Germany.

## Features
- **Tailored Stories**: Generates branching narratives appropriate for a specified age (default 12) using an LLM.
- **Vocabulary Support**: Advanced vocabulary in the story is highlighted. Hovering over a word reveals a simple English explanation.
- **GitHub Pages Integration**: The generated story is saved as a simple HTML page in the `docs/` folder, ready to be served by GitHub Pages.
- **Gradio Interface**: Easy-to-use UI for generating stories.

## Installation
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install gradio llm-client
   ```
   *Note: Ensure you have the `llm_client` from `dgaida/llm_client`.*

## Usage
1. Run the Gradio application:
   ```bash
   python src/app.py
   ```
2. Enter a topic and the age of the student.
3. Click "Generate and Add to Collection".
4. The story will be saved in `docs/stories/`.
5. Commit and push the changes to GitHub.

### 🚀 Enabling GitHub Pages
To host your stories, you must **manually enable** GitHub Pages in your repository settings:
1. Go to **Settings** > **Pages**.
2. Under **Build and deployment** > **Source**, select **GitHub Actions**.
3. Once enabled, every push to `main` that updates the `docs/` folder will automatically trigger a deployment.

## How it Works
- **Generation**: Uses the `llm_client` to prompt an LLM for a JSON-formatted branching story.
- **Frontend**: A JavaScript-based HTML template renders the story nodes and handles navigation between choices.
- **Vocabulary**: CSS tooltips are used for the mouse-over vocabulary explanations.

## License
MIT
