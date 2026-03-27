import json
from llm_client import LLMClient

def generate_story(topic, level="B1"):
    client = LLMClient()

    prompt = f"""
    Create a "choose your own adventure" story about "{topic}" for a student in Germany who is learning English at the CEFR {level} level.

    Guidelines:
    1. Language: English.
    2. Difficulty: Appropriate for the CEFR {level} level.
    3. Structure: A branching narrative with 10-15 nodes.
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
        print(f"Error parsing story JSON: {e}")
        print(f"Raw response: {response}")
        return None

if __name__ == "__main__":
    # Test generation
    story = generate_story("A mysterious forest", level="A2")
    if story:
        print(json.dumps(story, indent=2))
