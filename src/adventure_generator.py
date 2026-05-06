import logging
import json
from typing import Optional, Dict, Any
from llm_client import LLMClient

logger = logging.getLogger(__name__)

def generate_story(
    topic: str,
    level: str = "B1",
    length: str = "short (15-20 nodes)",
    age_range: str = "12-18"
) -> Optional[Dict[str, Any]]:
    """
    Generates a branching adventure story using an LLM.

    Args:
        topic: The description or theme of the story.
        level: The CEFR English level (A1, A2, B1, B2, C1, C2).
        length: The length of the story (number of nodes).
        age_range: The age range of the reader.

    Returns:
        A dictionary containing the story title, nodes, and vocabulary,
        or None if generation fails.
    """
    client = LLMClient(llm="openai/gpt-oss-120b", max_tokens=4096)

    prompt = f"""
    Create a "choose your own adventure" story about "{topic}" for a student in Germany who is learning English at the CEFR {level} level.
    The reader is in the age range: {age_range}. Ensure the content is age-appropriate and does not contain any adult content if the reader is a kid.

    Guidelines:
    1. Language: English.
    2. Difficulty: Appropriate for the CEFR {level} level.
    3. Structure: A branching narrative with {length}.
    4. Format: Return ONLY a JSON object with the following structure:
       {{
         "title": "Story Title",
         "nodes": {{
           "start": {{
             "text": "The opening paragraph...",
             "choices": [
               {{ "text": "Choice 1 text", "next_node": "node_id_1" }},
               {{ "text": "Choice 2 text", "next_node": "node_id_2" }}
             ]
           }},
           "node_id_1": {{
             "text": "Paragraph for node 1...",
             "choices": [...]
           }},
           ...
         }},
         "vocabulary": {{
           "word1": "simple English explanation",
           "word2": "simple English explanation"
         }}
       }}
    5. Vocabulary: Identify 10-20 difficult or advanced words used in the story and provide simple English explanations for them. IMPORTANT: Do not use any of the chosen vocabulary words within the explanations themselves, as this causes display issues.
    6. Ensure the JSON is valid and complete.
    """

    messages = [
        {"role": "system", "content": "You are a creative story writer and English teacher."},
        {"role": "user", "content": prompt}
    ]

    response = client.chat_completion(messages)

    # Try to extract JSON if the LLM added markdown markers
    try:
        if "```json" in response:
            json_str = response.split("```json")[1].split("```")[0].strip()
        elif "```" in response:
            json_str = response.split("```")[1].split("```")[0].strip()
        else:
            json_str = response.strip()

        story_data = json.loads(json_str)
        return story_data
    except Exception as e:
        logger.error(f"Error parsing story JSON: {e}")
        logger.error(f"Raw response: {response}")
        return None

if __name__ == "__main__":
    # Test generation
    story = generate_story("A mysterious forest", level="A2")
    if story:
        print(json.dumps(story, indent=2))
