import pytest
import json
from unittest.mock import MagicMock, patch
from adventure_generator import generate_story, validate_story_data, extract_json

@patch('adventure_generator.LLMClient')
def test_generate_story_two_agent_success(mock_client_class):
    # Mock LLMClient instances for Creator and Validator
    # Creator is called first, then Validator

    mock_creator_instance = MagicMock()
    mock_validator_instance = MagicMock()

    # Side effect to return different instances on subsequent calls
    mock_client_class.side_effect = [mock_creator_instance, mock_validator_instance]

    # Creator returns a valid story JSON
    story_json = json.dumps({
        "title": "Agent Story",
        "nodes": {
            "start": {"text": "Start", "choices": [{"text": "Next", "next_node": "end"}]},
            "end": {"text": "End", "choices": []}
        },
        "vocabulary": {"word": "desc"}
    })
    mock_creator_instance.chat_completion.return_value = story_json

    # Validator returns "VALID"
    mock_validator_instance.chat_completion.return_value = "VALID"

    result, raw = generate_story("Test", "B1")

    assert result is not None
    assert result['title'] == "Agent Story"
    assert raw == story_json

@patch('adventure_generator.LLMClient')
def test_generate_story_with_retry(mock_client_class):
    mock_creator_instance = MagicMock()
    mock_validator_instance = MagicMock()
    mock_client_class.side_effect = [mock_creator_instance, mock_validator_instance]

    # 1. Creator returns story with missing node
    story_v1 = json.dumps({
        "title": "Broken Story",
        "nodes": {
            "start": {"text": "Start", "choices": [{"text": "Next", "next_node": "missing"}]}
        },
        "vocabulary": {}
    })

    # 2. Creator returns fixed story
    story_v2 = json.dumps({
        "title": "Fixed Story",
        "nodes": {
            "start": {"text": "Start", "choices": [{"text": "Next", "next_node": "end"}]},
            "end": {"text": "End", "choices": []}
        },
        "vocabulary": {}
    })

    mock_creator_instance.chat_completion.side_effect = [story_v1, story_v2]

    # Validator fails first time, succeeds second
    mock_validator_instance.chat_completion.side_effect = ["Missing nodes!", "VALID"]

    result, raw = generate_story("Test")

    assert result is not None
    assert result['title'] == "Fixed Story"
    assert mock_creator_instance.chat_completion.call_count == 2
    assert mock_validator_instance.chat_completion.call_count == 2

def test_validate_story_data_success():
    story = {
        "title": "T",
        "nodes": {"start": {"text": "X", "choices": []}},
        "vocabulary": {}
    }
    valid, errors = validate_story_data(story)
    assert valid
    assert not errors

def test_validate_story_data_missing_node():
    story = {
        "title": "T",
        "nodes": {"start": {"text": "X", "choices": [{"text": "Y", "next_node": "Z"}]}},
        "vocabulary": {}
    }
    valid, errors = validate_story_data(story)
    assert not valid
    assert any("Missing nodes" in e for e in errors)

def test_extract_json():
    assert extract_json('{"a": 1}') == {"a": 1}
    assert extract_json('```json\n{"a": 1}\n```') == {"a": 1}
    assert extract_json('Plain text before\n```\n{"a": 1}\n```\nAfter') == {"a": 1}
    assert extract_json('Not JSON') is None
