import pytest
from unittest.mock import patch, MagicMock
from Buildqueryfromrules import load_rules, build_query_filters, apply_actions, process_emails
from models.model import Email

@pytest.fixture
def mock_session():
    """
    Fixture that provides a mock database session.
    This mock session can be used to simulate database operations in tests.
    """
    with patch('Buildqueryfromrules.SessionLocal') as mock_session_local:
        mock_session = MagicMock()
        mock_session_local.return_value = mock_session
        yield mock_session

@pytest.fixture
def mock_email_client():
    with patch('Buildqueryfromrules.EmailClientFactory') as mock_email_client_factory:
        mock_email_client = MagicMock()
        mock_email_client_factory.get_email_client.return_value = mock_email_client
        yield mock_email_client

def test_load_rules():
    with patch('builtins.open'), patch('json.load', return_value=[{"Rule": {}}]):
        rules = load_rules()
        assert rules == [{"Rule": {}}]

def test_build_query_filters(mock_session):
    """
    Test the build_query_filters function to ensure it generates the correct filters based on the given rule.
    """
    rule = { 
        "predicate": "all",
        "rules": [
            {"field": "Subject", "predicate": "contains", "value": "Test"}
        ]
    }
    filters = build_query_filters(rule, mock_session)
    expected_filters = [{"field": "Subject", "predicate": "contains", "value": "Test"}]
    assert filters == expected_filters

def test_apply_actions(mock_session, mock_email_client):
    emails = [MagicMock(id="1"), MagicMock(id="2")]
    actions = [{"action": "mark as read"}, {"action": "move to folder", "folder": "inbox"}]

    # Test that apply_actions correctly applies the given actions to the emails
    apply_actions(mock_session, emails, actions, "gmail")

    mock_email_client.mark_as_read.assert_called_once_with(["1", "2"])
    mock_email_client.move_email.assert_called_once_with({"1": "inbox", "2": "inbox"})

def test_process_emails(mock_session, mock_email_client):
    """
    Test the process_emails function to ensure it processes emails correctly based on rules.

    Args:
        mock_session (MagicMock): Mocked database session.
        mock_email_client (MagicMock): Mocked email client.

    Mocks:
        - Buildqueryfromrules.load_rules: Returns a predefined set of rules.
        - mock_session.query().filter().yield_per.return_value: Returns a list of mocked email objects.
        - mock_email_client.mark_as_read: Asserts that the function is called with the correct email IDs.

    Asserts:
        - The mark_as_read method of the email client is called once with the expected email IDs.
    """
    with patch('Buildqueryfromrules.load_rules', return_value=[{"Rule": {"predicate": "all", "rules": [{"field": "Subject", "predicate": "contains", "value": "Test"}], "actions": [{"action": "mark as read"}]}}]):
        process_emails("gmail")
        mock_session.query().filter().yield_per.return_value = [MagicMock(id="1"), MagicMock(id="2")]
        mock_email_client.mark_as_read.assert_called_once_with(["1", "2"])
