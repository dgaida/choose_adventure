import pytest
from unittest.mock import MagicMock, patch
from adventure_generator import generate_story

@patch('adventure_generator.LLMClient')
def test_generate_story_success(mock_client_class):
    # Setup mock
    mock_instance = mock_client_class.return_value
    mock_instance.chat_completion.return_value = '{"title": "Test Story", "nodes": {"start": {"text": "Once upon a time", "choices": []}}, "vocabulary": {}}'

    result = generate_story("A test topic", "B1", "short (15-20 nodes)", "12-18")

    assert result is not None
    assert result['title'] == "Test Story"
    assert "start" in result['nodes']

    # Verify LLMClient was initialized with the correct model and max_tokens
    mock_client_class.assert_called_once_with(llm="openai/gpt-oss-120b", max_tokens=4096)
    mock_instance.chat_completion.assert_called_once()

@patch('adventure_generator.LLMClient')
def test_generate_story_with_markdown(mock_client_class):
    # Setup mock with markdown
    mock_instance = mock_client_class.return_value
    mock_instance.chat_completion.return_value = '```json\n{"title": "Markdown Story", "nodes": {}, "vocabulary": {}}\n```'

    result = generate_story("A test topic", "B1")

    assert result is not None
    assert result['title'] == "Markdown Story"

@patch('adventure_generator.LLMClient')
def test_generate_story_failure(mock_client_class):
    # Setup mock with invalid JSON
    mock_instance = mock_client_class.return_value
    mock_instance.chat_completion.return_value = 'Invalid Response'

    result = generate_story("A test topic", "B1")

    assert result is None
