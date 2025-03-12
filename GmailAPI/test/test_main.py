import pytest
from unittest.mock import patch, MagicMock
import datetime
import email.utils as e
from main import fetch_and_store_emails

@pytest.fixture
def mock_db():
    """
    Mock the database session for testing purposes.

    This function uses the `patch` context manager from the `unittest.mock` module
    to replace the `SessionLocal` object in the `main` module with a mock object.
    It yields the mock database session object, which can be used in tests to
    simulate database interactions without requiring a real database connection.

    Yields:
        MagicMock: A mock database session object.
    """
    with patch('main.SessionLocal') as mock_session_local:
        mock_db = MagicMock()
        mock_session_local.return_value = mock_db
        yield mock_db

@pytest.fixture
def mock_email_client():
    with patch('main.EmailClientFactory') as mock_email_client:
        mock_email_client_instance = MagicMock()
        mock_email_client.get_email_client.return_value = mock_email_client_instance
        yield mock_email_client_instance

@patch('main.init_db')
def test_fetch_and_store_emails(mock_init_db, mock_db, mock_email_client):
    mock_email_client.fetch_emails.return_value = [
        {
            "id": "1",
            "From": "test@example.com",
            "Subject": "Test Subject",
            "message": "Test Message",
            "Date": "Mon, 25 Oct 2021 14:28:00 -0000",
            "To": "recipient@example.com",
            "Cc": "cc@example.com",
            "labels": "inbox"
        }
    ]
    mock_db.query().order_by().first.return_value = MagicMock(id="1")

    fetch_and_store_emails("gmail")

    mock_init_db.assert_called_once()
    mock_db.query().order_by().first.assert_called_once()
    mock_email_client.fetch_emails.assert_called_once_with("1")
    mock_db.merge.assert_called_once()
    mock_db.commit.assert_called_once()
