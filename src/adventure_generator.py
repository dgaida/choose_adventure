import logging
import json
from typing import Optional, Dict, Any, List
from llm_client import LLMClient

logger = logging.getLogger(__name__)


def validate_story_nodes(story_data: Dict[str, Any]) -> List[str]:
    """
    Checks if all nodes referenced in choices actually exist in the story.

    Returns:
        A list of missing node IDs.
    """
    nodes = story_data.get("nodes", {})
    referenced_nodes = set()

    for node_id, node_data in nodes.items():
        choices = node_data.get("choices", [])
        for choice in choices:
            next_node = choice.get("next_node")
            if next_node:
                referenced_nodes.add(next_node)

    missing_nodes = [
        node_id for node_id in referenced_nodes if node_id not in nodes
    ]
    return missing_nodes


def generate_story(
    topic: str,
    level: str = "B1",
    length: str = "short (15-25 nodes)",
    age_range: str = "12-18"
) -> tuple[Optional[Dict[str, Any]], str]:
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
    if "long" in length.lower():
        model = "llama-3.3-70b-versatile"
        max_tokens = 8192
    else:
        model = "openai/gpt-oss-120b"
        max_tokens = 8192

    client = LLMClient(llm=model, max_tokens=max_tokens)

    prompt = f"""
    Create a "choose your own adventure" story about "{topic}" for a student
    in Germany who is learning English at the CEFR {level} level.
    The reader is in the age range: {age_range}. Ensure the content is
    age-appropriate and does not contain any adult content if the reader
    is a kid.

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
    5. Node Integrity: Every "next_node" reference MUST point to a node that
       exists in the "nodes" dictionary. Avoid dead ends unless the story
       intentionally concludes.
    6. Vocabulary: Identify 10-20 difficult or advanced words used in the story
       and provide simple English explanations for them. IMPORTANT: Do not use
       any of the chosen vocabulary words within the explanations themselves,
       as this causes display issues.
    7. Ensure the JSON is valid and complete. Do not include any conversational
       text, explanations, or notes outside the JSON structure. Just return the
       JSON object.
    """

    messages = [
        {
            "role": "system",
            "content": (
                "You are a creative story writer and English teacher. "
                "You must follow the storytelling skill described in "
                "choose_your_own_adventure_story_skill.md "
                "(https://github.com/dgaida/choose_adventure/blob/main/"
                "choose_your_own_adventure_story_skill.md): "
                "create highly engaging interactive stories with meaningful "
                "choices, high momentum, suspenseful cliffhangers, and "
                "emotionally difficult decisions. Ensure every choice "
                "matters and the narrative reacts to the reader's decisions."
            )
        },
        {"role": "user", "content": prompt}
    ]

    attempts = 0
    max_attempts = 3
    last_response = ""

    while attempts < max_attempts:
        attempts += 1
        last_response = client.chat_completion(messages)

        # Try to extract JSON
        try:
            if "```json" in last_response:
                json_str = last_response.split("```json")[1].split(
                    "```"
                )[0].strip()
            elif "```" in last_response:
                json_str = last_response.split("```")[1].split(
                    "```"
                )[0].strip()
            else:
                json_str = last_response.strip()

            story_data = json.loads(json_str)

            # Validate nodes
            missing_nodes = validate_story_nodes(story_data)
            if not missing_nodes:
                return story_data, last_response

            logger.warning(
                f"Attempt {attempts}: Missing nodes detected: {missing_nodes}"
            )

            # Update messages for the next attempt
            messages.append({"role": "assistant", "content": last_response})
            error_message = (
                f"The generated story has references to missing nodes: "
                f"{missing_nodes}. Please fix the story so that all "
                f"referenced nodes exist in the \"nodes\" dictionary."
            )
            messages.append({"role": "user", "content": error_message})

        except Exception as e:
            logger.error(
                f"Error parsing story JSON on attempt {attempts}: {e}"
            )
            if attempts == max_attempts:
                return None, last_response

            # Ask the LLM to provide valid JSON if it failed parsing
            messages.append({"role": "assistant", "content": last_response})
            messages.append({
                "role": "user",
                "content": "The JSON was invalid. Please return a valid JSON."
            })

    return None, last_response


if __name__ == "__main__":
    # Test generation
    story = generate_story("A mysterious forest", level="A2")
    if story:
        print(json.dumps(story, indent=2))
