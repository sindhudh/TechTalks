from clients.gmail_client import GmailClient

class EmailClientFactory:
    """Factory class to return the appropriate email client"""
    
    @staticmethod
    def get_email_client(provider: str):
        if provider.lower() == "gmail":
            return GmailClient()
        else:
            raise ValueError(f"Unsupported email provider: {provider}")
