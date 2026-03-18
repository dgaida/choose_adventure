# Adventure Story Generator

[![Auto Versioning & Badges](https://github.com/dgaida/adventure-story-generator/actions/workflows/versioning-and-badges.yml/badge.svg)](https://github.com/dgaida/adventure-story-generator/actions/workflows/versioning-and-badges.yml)
[![Version](https://img.shields.io/github/v/tag/dgaida/choose_adventure?label=version)](https://github.com/dgaida/choose_adventure/tags)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docs](https://img.shields.io/badge/docs-GitHub%20Pages-blue)](https://dgaida.github.io/choose_adventure/)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/dgaida/choose_adventure/graphs/commit-activity)
![Last commit](https://img.shields.io/github/last-commit/dgaida/choose_adventure)

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
3. Click "Generate and Publish Story".
4. The story will be saved to `docs/index.html`.
5. Commit and push the changes to GitHub. If GitHub Pages is enabled for the `docs/` folder, your story will be live!

## How it Works
- **Generation**: Uses the `llm_client` to prompt an LLM for a JSON-formatted branching story.
- **Frontend**: A JavaScript-based HTML template renders the story nodes and handles navigation between choices.
- **Vocabulary**: CSS tooltips are used for the mouse-over vocabulary explanations.

## License
MIT
