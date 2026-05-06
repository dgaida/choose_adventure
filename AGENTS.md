# Agent Instructions for Adventure Story Generator

This repository contains a "choose your own adventure" story generator designed for English learners in Germany.

## Project Structure  
- `src/`: Python source code.  
  - `app.py`: Gradio interface and main application logic.  
  - `adventure_generator.py`: LLM integration via `llm_client`.  
  - `update_manifest.py`: Utility to update the story manifest.  
  - `templates/story_template.html`: Template for the generated story page.  
- `docs/`: Static HTML content for GitHub Pages.  
  - `index.html`: The main story viewer, initialized from `src/templates/story_template.html`.  
  - `stories/`: JSON files containing generated stories and `manifest.json`.  

## Core Logic & Conventions  
- **Vocabulary Highlighting**: The story viewer uses a single-pass regex in `highlightVocab` to apply tooltips. This prevents recursive tagging if an explanation contains another vocabulary word. Always maintain this logic in `docs/index.html` and `src/templates/story_template.html`.  
- **LLM Integration**: Use the `llm_client` library for all LLM calls. The prompt should ensure the output is valid JSON and that vocabulary words are not used in their own definitions.  
- **CEFR Levels**: Stories are categorized by CEFR levels (A1, A2, B1, B2, C1, C2).  

## Deployment  
- The app is designed for deployment on Render.com (controlled by `render.yaml`).  
- Story hosting is handled via GitHub Pages. The `.github/workflows/docs.yml` action automatically updates the manifest and deploys the `docs/` folder.  

## Development Setup  
- Install dependencies: `pip install -r requirements.txt`  
- Set `PYTHONPATH` to `src` when running scripts locally: `export PYTHONPATH=$PYTHONPATH:$(pwd)/src`  

## Repository Health & Maintenance  
- **Testing**: A test suite exists in `tests/`. Always run `pytest` before submitting changes.  
- **Temporary Files**: Do not commit log files (`*.log`) or temporary verification scripts (`verify_*.py`, `verify_*.js`) to the repository.  
- **Code Standards**: Maintain type hints and descriptive docstrings for all new Python functions.  
