import pytest
import os
import json
from unittest.mock import MagicMock, patch
from app import create_github_pr

@patch('app.Github')
@patch('os.environ.get')
def test_create_github_pr_success(mock_env_get, mock_github_class):
    # Mock environment variables
    mock_env_get.side_effect = lambda k, default=None: {
        "GITHUB_TOKEN": "fake-token",
        "GITHUB_REPO": "owner/repo"
    }.get(k, default)

    # Mock GitHub objects
    mock_github_instance = mock_github_class.return_value
    mock_repo = MagicMock()
    mock_github_instance.get_repo.return_value = mock_repo

    mock_repo.default_branch = "main"
    mock_branch = MagicMock()
    mock_repo.get_branch.return_value = mock_branch
    mock_branch.commit.sha = "base-sha"

    mock_manifest_file = MagicMock()
    mock_manifest_file.decoded_content = b'{"stories": []}'
    mock_manifest_file.sha = "manifest-sha"
    mock_repo.get_contents.return_value = mock_manifest_file

    mock_pr = MagicMock()
    mock_pr.html_url = "https://github.com/owner/repo/pull/1"
    mock_repo.create_pull.return_value = mock_pr

    story_data = {
        "title": "Test Story",
        "nodes": {"start": {"text": "Once...", "choices": []}},
        "vocabulary": {}
    }

    result = create_github_pr(json.dumps(story_data))

    assert "Pull Request created successfully" in result
    assert "https://github.com/owner/repo/pull/1" in result

    # Verify GitHub API calls
    mock_github_class.assert_called_once_with("fake-token")
    mock_github_instance.get_repo.assert_called_once_with("owner/repo")
    mock_repo.create_git_ref.assert_called_once()
    mock_repo.create_file.assert_called_once()
    mock_repo.update_file.assert_called_once()
    mock_repo.create_pull.assert_called_once()

@patch('os.environ.get')
def test_create_github_pr_no_token(mock_env_get):
    mock_env_get.return_value = None

    result = create_github_pr(json.dumps({"title": "Test"}))
    assert "Error: GITHUB_TOKEN environment variable not set" in result

def test_create_github_pr_no_data():
    result = create_github_pr("")
    assert "Error: No story data found" in result

def test_create_github_pr_invalid_json():
    result = create_github_pr("not a json")
    assert "Error: Invalid JSON" in result
