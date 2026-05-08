import pytest
from unittest.mock import MagicMock, patch
from adventure_generator import generate_story

@patch('adventure_generator.LLMClient')
def test_generate_story_short_success(mock_client_class):
    # Setup mock
    mock_instance = mock_client_class.return_value
    mock_instance.chat_completion.return_value = '{"title": "Short Story", "nodes": {"start": {"text": "Once upon a time", "choices": []}}, "vocabulary": {}}'

    result, raw = generate_story("A test topic", "B1", "short (15-20 nodes)", "12-18")

    assert result is not None
    assert isinstance(raw, str)
    assert result['title'] == "Short Story"

    # Verify LLMClient was initialized with the correct model and max_tokens for short story
    mock_client_class.assert_called_once_with(llm="openai/gpt-oss-120b", max_tokens=8000)
    mock_instance.chat_completion.assert_called_once()

@patch('adventure_generator.LLMClient')
def test_generate_story_long_success(mock_client_class):
    # Setup mock
    mock_instance = mock_client_class.return_value
    mock_instance.chat_completion.return_value = '{"title": "Long Story", "nodes": {"start": {"text": "A long time ago", "choices": []}}, "vocabulary": {}}'

    result, raw = generate_story("A test topic", "B1", "long (35-50 nodes)", "12-18")

    assert result is not None
    assert isinstance(raw, str)
    assert result['title'] == "Long Story"

    # Verify LLMClient was initialized with the correct model and max_tokens for long story
    mock_client_class.assert_called_once_with(llm="llama-3.3-70b-versatile", max_tokens=12000)
    mock_instance.chat_completion.assert_called_once()

@patch('adventure_generator.LLMClient')
def test_generate_story_with_markdown(mock_client_class):
    # Setup mock with markdown
    mock_instance = mock_client_class.return_value
    mock_instance.chat_completion.return_value = '```json\n{"title": "Markdown Story", "nodes": {}, "vocabulary": {}}\n```'

    result, raw = generate_story("A test topic", "B1")

    assert result is not None
    assert isinstance(raw, str)
    assert result['title'] == "Markdown Story"

@patch('adventure_generator.LLMClient')
def test_generate_story_failure(mock_client_class):
    # Setup mock with invalid JSON
    mock_instance = mock_client_class.return_value
    mock_instance.chat_completion.return_value = 'Invalid Response'

    result, raw = generate_story("A test topic", "B1")

    assert result is None
    assert raw == "Invalid Response"

@patch('adventure_generator.LLMClient')
def test_generate_story_empty_response(mock_client_class):
    # Setup mock with empty response
    mock_instance = mock_client_class.return_value
    mock_instance.chat_completion.return_value = ''

    result, raw = generate_story("A test topic", "B1")

    assert result is None
    assert raw == ''

from adventure_generator import validate_story_nodes

def test_validate_story_nodes_success():
    story_data = {
        "nodes": {
            "start": {
                "choices": [
                    {"next_node": "node1"},
                    {"next_node": "node2"}
                ]
            },
            "node1": {"choices": []},
            "node2": {"choices": []}
        }
    }
    assert validate_story_nodes(story_data) == []

def test_validate_story_nodes_missing():
    story_data = {
        "nodes": {
            "start": {
                "choices": [
                    {"next_node": "node1"},
                    {"next_node": "missing_node"}
                ]
            },
            "node1": {"choices": []}
        }
    }
    assert validate_story_nodes(story_data) == ["missing_node"]

def test_validate_story_nodes_no_choices():
    story_data = {
        "nodes": {
            "start": {"text": "End of story"}
        }
    }
    assert validate_story_nodes(story_data) == []
