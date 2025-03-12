from abc import ABC, abstractmethod

class BaseEmailClient(ABC):
    """Abstract base class for email clients"""

    @abstractmethod
    def authenticate(self):
        """Authenticate with the email service"""
        pass

    @abstractmethod
    def fetch_emails(self,lastid, max_results=10):
        """Fetch a list of emails"""
        pass

    @abstractmethod
    def mark_as_read(self, email_id):
        """Mark an email as read"""
        pass

    @abstractmethod
    def move_email(self, email_id, folder_name):
        """Move an email to a specified folder"""
        pass
