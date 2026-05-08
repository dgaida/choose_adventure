import logging
import json
from typing import Optional, Dict, Any, List, Tuple
from pydantic import BaseModel, Field, ValidationError, model_validator
from llm_client import LLMClient

logger = logging.getLogger(__name__)

# --- Pydantic Models for Validation ---

class Choice(BaseModel):
    text: str
    next_node: str

class StoryNode(BaseModel):
    text: str
    choices: List[Choice] = Field(default_factory=list)

class StoryModel(BaseModel):
    title: str
    nodes: Dict[str, StoryNode]
    vocabulary: Dict[str, str]

    @model_validator(mode='after')
    def check_node_integrity(self) -> 'StoryModel':
        referenced_nodes = set()
        for node_id, node_data in self.nodes.items():
            for choice in node_data.choices:
                referenced_nodes.add(choice.next_node)

        missing = [node_id for node_id in referenced_nodes if node_id not in self.nodes]
        if missing:
            raise ValueError(f"Missing nodes referenced in choices: {missing}")
        return self

# --- Helper Functions ---

def validate_story_data(story_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Validates the story data using Pydantic.
    Returns (is_valid, list_of_errors).
    """
    try:
        StoryModel(**story_data)
        return True, []
    except ValidationError as e:
        errors = []
        for error in e.errors():
            loc = " -> ".join(str(x) for x in error['loc'])
            errors.append(f"{loc}: {error['msg']}")
        return False, errors
    except Exception as e:
        return False, [str(e)]

def extract_json(response: str) -> Optional[Dict[str, Any]]:
    """Extracts JSON from an LLM response string."""
    try:
        if "```json" in response:
            json_str = response.split("```json")[1].split("```")[0].strip()
        elif "```" in response:
            json_str = response.split("```")[1].split("```")[0].strip()
        else:
            json_str = response.strip()
        return json.loads(json_str)
    except Exception:
        return None

# --- Agent Implementation ---

class CreatorAgent:
    def __init__(self, model: str, max_tokens: int):
        self.client = LLMClient(llm=model, max_tokens=max_tokens)
        self.system_prompt = (
            "You are a creative story writer and English teacher. "
            "You follow the storytelling skill: create highly engaging "
            "interactive stories with meaningful choices, high momentum, "
            "suspenseful cliffhangers, and emotionally difficult decisions. "
            "Ensure every choice matters and the narrative reacts to the "
            "reader's decisions."
        )

    def generate(self, prompt: str, history: List[Dict[str, str]] = None) -> str:
        messages = [{"role": "system", "content": self.system_prompt}]
        if history:
            messages.extend(history)
        messages.append({"role": "user", "content": prompt})
        return self.client.chat_completion(messages)

class ValidatorAgent:
    def __init__(self, model: str, max_tokens: int):
        # We can use the same or a different model for validation
        self.client = LLMClient(llm=model, max_tokens=max_tokens)
        self.system_prompt = (
            "You are a meticulous story editor and validator. "
            "Your job is to ensure that stories are structurally sound, "
            "meaningful, and follow all guidelines. You check for "
            "logical consistency, age-appropriateness, and node integrity."
        )

    def validate(self, story_json: str, validation_errors: List[str]) -> Tuple[bool, str]:
        prompt = f"""
        Please validate the following "choose your own adventure" story.

        Story JSON:
        {story_json}

        Automated Validation Errors:
        {json.dumps(validation_errors, indent=2)}

        Task:
        1. Review the story for logical consistency and engagement.
        2. If there are missing nodes or structural issues, identify exactly where they are.
        3. Check if the CEFR level and age-appropriateness are met.
        4. If everything is perfect, respond with "VALID".
        5. If there are issues, provide a clear, concise list of what needs to be fixed.
        """

        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": prompt}
        ]

        response = self.client.chat_completion(messages)
        is_valid = response.strip().upper() == "VALID"
        return is_valid, response

def generate_story(
    topic: str,
    level: str = "B1",
    length: str = "short (15-25 nodes)",
    age_range: str = "12-18"
) -> tuple[Optional[Dict[str, Any]], str]:
    """
    Generates a branching adventure story using a two-agent workflow.
    """
    if "long" in length.lower():
        model = "llama-3.3-70b-versatile"
        max_tokens = 8192
    else:
        model = "openai/gpt-oss-120b"
        max_tokens = 8192

    creator = CreatorAgent(model, max_tokens)
    validator = ValidatorAgent(model, max_tokens)

    initial_prompt = f"""
    Create a "choose your own adventure" story about "{topic}" for a student
    in Germany who is learning English at the CEFR {level} level.
    The reader is in the age range: {age_range}.

    Guidelines:
    1. Language: English. CEFR Level: {level}.
    2. Structure: A branching narrative with {length}.
    3. Format: Return ONLY a JSON object with:
       {{
         "title": "Story Title",
         "nodes": {{
           "start": {{ "text": "...", "choices": [{{ "text": "...", "next_node": "node_id_1" }}] }},
           "node_id_1": {{ "text": "...", "choices": [...] }}
         }},
         "vocabulary": {{ "word": "explanation" }}
       }}
    4. Node Integrity: Every "next_node" MUST exist.
    5. Vocabulary: 10-20 words with simple English explanations. Do not use the word in its explanation.
    """

    attempts = 0
    max_attempts = 3
    history = []
    last_creator_response = ""

    while attempts < max_attempts:
        attempts += 1
        logger.info(f"Generation attempt {attempts}...")

        last_creator_response = creator.generate(initial_prompt if attempts == 1 else "Fix the issues reported by the validator.", history)

        story_data = extract_json(last_creator_response)
        if not story_data:
            logger.warning(f"Attempt {attempts}: Failed to extract JSON.")
            history.append({"role": "assistant", "content": last_creator_response})
            history.append({"role": "user", "content": "The output was not valid JSON. Please return ONLY the JSON object."})
            continue

        # Programmatic validation
        is_structurally_valid, errors = validate_story_data(story_data)

        # Agent validation
        is_agent_valid, feedback = validator.validate(json.dumps(story_data), errors)

        if is_structurally_valid and is_agent_valid:
            logger.info("Story validated successfully.")
            return story_data, last_creator_response

        logger.warning(f"Attempt {attempts}: Validation failed. Feedback: {feedback}")

        # Provide feedback to creator
        history.append({"role": "assistant", "content": last_creator_response})
        feedback_msg = f"The validator found issues with your story:\n\n{feedback}\n\n"
        if errors:
            feedback_msg += f"Structural Errors:\n{json.dumps(errors, indent=2)}\n\n"
        feedback_msg += "Please fix these issues and provide the complete, updated story JSON."

        history.append({"role": "user", "content": feedback_msg})

    return extract_json(last_creator_response), last_creator_response

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    story, raw = generate_story("A space adventure", level="A2")
    if story:
        print(f"Success: {story.get('title')}")
    else:
        print("Failed to generate story.")
