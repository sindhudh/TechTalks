import pytest
from unittest.mock import patch, MagicMock
from clients.gmail_client import GmailClient

@pytest.fixture
def gmail_client():
    yield GmailClient()

@patch('clients.gmail_client.GmailClient.authenticate', return_value=MagicMock())
def test_authenticate(mock_authenticate, gmail_client):
    gmail_client.authenticate()
    mock_authenticate.assert_called_once()
    assert gmail_client.service is not None, "The GmailClient service should not be None after authentication."

@patch('clients.gmail_client.build')
@patch('clients.gmail_client.Credentials')
@patch('clients.gmail_client.InstalledAppFlow')
def test_authenticate_flow(mock_flow, mock_creds, mock_build):
    mock_creds.from_authorized_user_file.return_value = None
    mock_flow.from_client_secrets_file.return_value.run_local_server.return_value = MagicMock()
    mock_build.return_value = MagicMock()

    client = GmailClient()
    assert client.service is not None

def test_fetch_emails(gmail_client):
    """
    Test the fetch_emails method of the GmailClient class.
    This test mocks the Gmail API service to simulate fetching emails. It sets up the mock service to return a predefined list of messages and a specific message payload when the list and get methods are called, respectively. The test then calls the fetch_emails method with a dummy lastid and asserts that the returned emails list contains one email with the expected subject.
    Args:
        gmail_client (GmailClient): An instance of the GmailClient class.
    Assertions:
        - The length of the returned emails list is 1.
        - The subject of the first email in the list is "Test Subject".
    """
    mock_service = gmail_client.service
    mock_service.users().messages().list().execute.return_value = {
        "messages": [{"id": "1"}]
    }
    mock_service.users().messages().get().execute.return_value = {
        "payload": {"headers": [{"name": "Subject", "value": "Test Subject"}, {"name": "From", "value": "test@example.com"}, {"name": "Date", "value": "Mon, 25 Oct 2021 14:28:00 -0000"}]},
        "snippet": "Test Message",
        "labelIds": ["INBOX"]
    }

    emails = gmail_client.fetch_emails("lastid")
    assert len(emails) == 1
    assert emails[0]["Subject"] == "Test Subject"

def test_mark_as_read(gmail_client):
    """
    Test the mark_as_read method of the GmailClient class.
    This test mocks the Gmail API service to simulate marking emails as read. It sets up the mock service to return a mock batch request and verifies that the mark_as_read method adds the correct number of requests to the batch and executes it.
    Args:
        gmail_client (GmailClient): An instance of the GmailClient class.
    Assertions:
        - The number of requests added to the batch is 2.
        - The batch execute method is called once.
    """
    mock_service = gmail_client.service
    mock_batch = MagicMock()
    mock_service.new_batch_http_request.return_value = mock_batch

    gmail_client.mark_as_read(["1", "2"])
    assert mock_batch.add.call_count == 2
    mock_batch.execute.assert_called_once()

def test_move_email(gmail_client):
    mock_service = gmail_client.service
    mock_batch = MagicMock()
    mock_service.new_batch_http_request.return_value = mock_batch

    gmail_client.move_email({"1": "Label_1", "2": "Label_2"})
    assert mock_batch.add.call_count == 2
    mock_batch.execute.assert_called_once()
