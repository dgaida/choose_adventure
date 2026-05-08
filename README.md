# Adventure Story Generator

[![Auto Versioning & Badges](https://github.com/dgaida/adventure-story-generator/actions/workflows/versioning-and-badges.yml/badge.svg)](https://github.com/dgaida/adventure-story-generator/actions/workflows/versioning-and-badges.yml)
[![Version](https://img.shields.io/github/v/tag/dgaida/choose_adventure?label=version)](https://github.com/dgaida/choose_adventure/tags)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docs](https://img.shields.io/badge/docs-GitHub%20Pages-blue)](https://dgaida.github.io/choose_adventure/)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/dgaida/choose_adventure/graphs/commit-activity)
![Last commit](https://img.shields.io/github/last-commit/dgaida/choose_adventure)
[![Code Quality](https://github.com/dgaida/choose_adventure/actions/workflows/lint.yml/badge.svg)](https://github.com/dgaida/choose_adventure/actions/workflows/lint.yml)
[![CodeQL](https://github.com/dgaida/choose_adventure/actions/workflows/codeql.yml/badge.svg)](https://github.com/dgaida/choose_adventure/actions/workflows/codeql.yml)

A "choose your own adventure" story generator for English learners in Germany.

## Live Demo
You can try the generator live at: [https://choose-adventure.onrender.com/](https://choose-adventure.onrender.com/)

## Features  
- **Tailored Stories**: Generates branching narratives appropriate for a specified age (default 12) using an LLM.  
- **Storytelling Skill**: Uses a specialized "Choose-Your-Own-Adventure Storytelling Skill" to ensure high-quality, reactive, and engaging narratives.  
- **Vocabulary Support**: Advanced vocabulary in the story is highlighted. Hovering over a word reveals a simple English explanation.  
- **GitHub Pages Integration**: The generated story is saved as a simple HTML page in the `docs/` folder, ready to be served by GitHub Pages.  
- **Gradio Interface**: Easy-to-use UI for generating stories.  

## Getting Started: API Keys
To generate stories, you will need an API Key for one of the supported LLM providers. You can follow these tutorials to create your keys:  
- [Creating a Groq API Key](https://dgaida.github.io/llm_client/dev/en/tutorials/rag-chatbot/#creating-a-groq-api-key)  
- [Creating a Google Gemini API Key](https://dgaida.github.io/llm_client/dev/en/tutorials/rag-chatbot/#creating-a-google-gemini-api-key)  
- [Creating an OpenAI API Key](https://dgaida.github.io/llm_client/dev/en/tutorials/rag-chatbot/#creating-an-openai-api-key)  

## Installation  
1. Clone the repository.  
2. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```
   *Note: Ensure you have the `llm_client` from `dgaida/llm_client`.*

## Usage  
1. Run the Gradio application:  
   ```bash
   python src/app.py
   ```
2. Enter your **LLM API Key** in the provided field.  
3. Enter a story description and select the English level (A1-C2).  
4. Click "Generate Story".  
5. The story will be saved in `docs/stories/`.  
6. Review the preview and click "Create Pull Request on GitHub" to submit it to the collection.  

### 🚀 Deploying to Render.com
You can host the Gradio interface on Render.com:  
1. Create a new **Web Service** on Render.  
2. Connect your GitHub repository.  
3. Render will automatically detect the `render.yaml` file (Blueprint) or you can manually configure:  
   - **Runtime**: `Python`  
   - **Build Command**: `pip install -r requirements.txt`  
   - **Start Command**: `python src/app.py`  
4. Add an environment variable `PORT` set to `7860`.  
5. The app will be available at your Render URL.  

### 🚀 Enabling GitHub Pages
To host your stories, you must **manually enable** GitHub Pages in your repository settings:  
1. Go to **Settings** > **Pages**.  
2. Under **Build and deployment** > **Source**, select **GitHub Actions**.  
3. Once enabled, every push to `main` that updates the `docs/` folder will automatically trigger a deployment.  

## How it Works  
- **Generation**: Uses the `llm_client` to prompt an LLM for a JSON-formatted branching story, following the storytelling skill.  
- **Frontend**: A JavaScript-based HTML template renders the story nodes and handles navigation between choices.  
- **Vocabulary**: CSS tooltips are used for the mouse-over vocabulary explanations.  

## License
MIT
